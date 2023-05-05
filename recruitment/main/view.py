from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.views import View
from main.models import Candidate, CBISchedule, Status, Source
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from main.auth import CustomLoginRequired
from main.utils import return_json
from django.db.models import Q, Case, When, CharField, Value, Count, OuterRef, Subquery, F
from django.utils import timezone
from querystring_parser import parser
from datetime import datetime

# Create your views here.
def index(request):
    return JsonResponse('Hello world',safe=False)
    

class BrowseIndex(CustomLoginRequired, View):

    def get(self,request:HttpRequest):

        # return JsonResponse(parser.parse(request.get_full_path().split('?')[1]),safe=False)

        if not return_json(request): # first view load

            #fetch statuses
            lst_sources = list(Source.objects.all().values())
            lst_statuses = Status.objects.all().values('codename','status')
            statuses = dict(
                initscreening=[],
                prescreening=[],
                cbi=[],
                gpt=[],
                overall_status=[],
            )
            for status_obj in lst_statuses:
                codename:str = status_obj['codename']
                status:str = status_obj['status']
                out_status = {'codename':codename,'status':status}

                stage,phase = tuple(codename.split(':'))
                if phase == 'ongoing': # overall_status
                    statuses['overall_status'].append(out_status)
                elif stage in ('initscreening','prescreening') :
                    if phase in ('pending','proceed','not proceed'):
                        statuses[stage].append(out_status)
                elif stage == 'cbi':
                    if phase in ('pending interview','pending result','proceed','not proceed'):
                        statuses[stage].append(out_status)
                elif stage == 'gpt_status':
                    statuses['gpt'].append(out_status)

            
            # Get the start and end of the current week
            today = timezone.now().date()
            start_of_week = today - timezone.timedelta(days=today.weekday())
            end_of_week = start_of_week + timezone.timedelta(days=6)

            # fetch action metrics
            latest_cbischedule_status = CBISchedule.objects.filter(cbi__candidate=OuterRef('pk')).order_by('-created_at').values('status__codename')[:1]
            metrics = Candidate.objects.annotate(
                latest_cbischedule_status = Subquery(latest_cbischedule_status),
            ).aggregate(
                pending_initial_screening=Count(
                    'id',
                    filter=
                        Q(initialscreening__status__isnull=False) & 
                        ~Q(initialscreening__status__codename="proceed") & 
                        Q(prescreening__status__isnull=True) &
                        Q(cbi__status__isnull=True)
                ),
                pending_prescreening=Count(
                    'id',
                    filter=
                        ~Q(prescreening__status__codename="proceed") & 
                        Q(prescreening__status__isnull=False) &
                        Q(cbi__status__isnull=True)
                ),
                ready_interview=Count(
                    'id',
                    filter=
                        Q(cbi__status__isnull=False) &
                        Q(latest_cbischedule_status="proceed")
                ),
                new_application=Count(
                    'id',
                    filter=
                        Q(date__range=(start_of_week,end_of_week))
                )
            )

            return render(request,'main/browse.html',{"metrics":metrics, 'statuses':statuses, 'source':lst_sources})

        candidates = Candidate.objects
        
        # handle table manipulation (filtering, sorting)
        
        try:
            dt_query_params = parser.parse(request.get_full_path().split('?')[1])
        except IndexError:
            dt_query_params = {}

        
        # individual column filtering
        if 'columns' in dt_query_params:
            for dt_column in dt_query_params['columns'].values():
                
                dt_filter_val = dt_column['search']['value']
                
                if bool(dt_filter_val):
                    dt_attr:str = dt_column['data']
                    # name, date
                    if dt_attr == 'name':
                        candidates = candidates.filter(**{f"{dt_attr}__contains":dt_filter_val})
                    elif dt_attr == 'date':
                        candidates = candidates.filter(**{f"{dt_attr}":datetime.strptime(dt_filter_val,'%Y-%m-%d').date()})
                    else:
                        dt_attr = dt_attr.rsplit('_',1)[0]
                        
                        # source,
                        if dt_attr == 'source':
                            candidates = candidates.filter(**{f"{dt_attr}__id":dt_filter_val})
                        # gpt_status, overall_status    
                        elif dt_attr in ('gpt_status','overall_status'):
                            candidates = candidates.filter(**{f"{dt_attr}__codename":dt_filter_val})
                        # initialscreening, prescreening, cbi,
                        else:
                            candidates = candidates.filter(**{f"{dt_attr}__status__codename":dt_filter_val})

        
        # fetch list of candidates
        
        candidates = candidates.values(
            'id',
            'name',
            'date',
            overall_status_name=F('overall_status__status'),
            source_name=F('source__source'),
            gpt_status_name=F('gpt_status__status'),
            initialscreening_status=Case(
                When(Q(initialscreening__status__status__isnull=False),then=F('initialscreening__status__status')),
                default=Value('-')
            ),
            prescreening_status=Case(
                When(Q(prescreening__status__status__isnull=False),then=F('prescreening__status__status')),
                default=Value('-')
            ),
            cbi_status=Case(
                When(Q(cbi__status__status__isnull=False),then=F('cbi__status__status')),
                default=Value('-')
            ),
        )

        # sorting
        if 'order' in dt_query_params:
            order_bys = list()
            
            for dt_order in dt_query_params['order'].values():
                dt_attr:str = dt_query_params['columns'][int(dt_order['column'])]['data']
                order_bys.append(f"{'' if dt_order['dir'] == 'asc' else '-'}{dt_attr}")
            
            candidates = candidates.order_by(*order_bys)


        # Get pagination parameters from request
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))

        # Create a Paginator object for the queryset
        paginator = Paginator(candidates, length)

        # Get the current page of data
        page_number = start // length + 1
        page_obj = paginator.get_page(page_number)
        
        # Convert the data to a format that DataTables expects
        data = {
            'draw': request.GET.get('draw', 1),
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count,
            'data': [
                obj for obj in page_obj.object_list
            ],
        }
        
        
        return JsonResponse(data)
    
class BrowseView(CustomLoginRequired, View):

    def get(self,request:HttpRequest,candidate_id):
        
        return JsonResponse(list(Candidate.objects.filter(id=candidate_id).values()),safe=False)
