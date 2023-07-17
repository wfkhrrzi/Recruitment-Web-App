from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.views import View
from main.models import Candidate, CBISchedule, Status, Source, CBI, Prescreening, InitialScreening, CandidateResume, EmpCategory
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from main.auth import CustomLoginRequired
from main.utils import return_json
from django.db.models import Q, Case, When, Value, Count, OuterRef, Subquery, F, CharField, TextField
from django.db.models.functions import Concat, Cast
from django.utils import timezone
from querystring_parser import parser
from django.urls import reverse
from datetime import datetime

# Create your views here.
def index(request):
    # return JsonResponse('Hello world',safe=False)
    return render(request,'main/pages/home.html')
    

class BrowseIndex(CustomLoginRequired, View):

    def get(self,request:HttpRequest,template_name='main/pages/browse.html'):

        # Get the start and end of the current week
        today = timezone.now().date()
        # start_of_week = today - timezone.timedelta(days=today.weekday())
        start_of_week = today - timezone.timedelta(days=6)
        end_of_week = start_of_week + timezone.timedelta(days=6)

        if not return_json(request): # first view load

            #fetch statuses
            lst_category = list(EmpCategory.objects.all().values())
            lst_sources = list(Source.objects.all().values())
            lst_statuses = Status.objects.all().values('pk','codename','status')
            statuses = dict(
                initscreening=[],
                prescreening=[],
                cbi=[],
                gpt_status=[],
                overall_status=[],
            )
            for status_obj in lst_statuses:
                codename:str = status_obj['codename']
                status:str = status_obj['status']
                id:int = status_obj['pk']
                out_status = {'id':id,'codename':codename,'status':status}

                stage,phase = tuple(codename.split(':'))
                if id in [obj['overall_status'] for obj in list(Candidate.objects.values('overall_status').distinct())]: # overall_status
                    statuses['overall_status'].append(out_status)
                elif stage == 'initscreening' :
                    if phase in ('pending','selected','not selected'):
                        statuses[stage].append(out_status)
                elif stage in ('prescreening','cbi','gpt_status',):
                    statuses[stage].append(out_status)

                # elif stage == 'prescreening':
                #     if phase in ('pending','proceed','not proceed'):
                #         statuses[stage].append(out_status)
                # elif stage == 'cbi':
                #     if phase in ('pending interview','pending result','proceed','not proceed'):
                #         statuses[stage].append(out_status)
                # elif stage == 'gpt_status':
                #     statuses['gpt'].append(out_status)


            # fetch action metrics
            latest_cbischedule_status = CBISchedule.objects.filter(cbi__candidate=OuterRef('pk')).order_by('-created_at').values('is_proceed')[:1]
            metrics = Candidate.objects.annotate(
                latest_cbischedule_status = Subquery(latest_cbischedule_status),
            ).aggregate(
                # new_application=Count(
                #     'id',
                #     filter=
                #         Q(date__range=(start_of_week,today))
                # ),
                pending_initial_screening=Count(
                    'id',
                    filter=
                        # Q(initialscreening__status__isnull=False) & 
                        ~Q(initialscreening__status__codename__in=["initscreening:selected","initscreening:not selected"]) & 
                        Q(prescreening__status__isnull=True) &
                        Q(cbi__status__isnull=True)
                ),
                pending_preassessment=Count(
                    'id',
                    filter=
                        ~Q(prescreening__status__codename="prescreening:proceed") & 
                        Q(prescreening__status__isnull=False) &
                        Q(cbi__status__isnull=True)
                ),
                ready_interview=Count(
                    'id',
                    filter=
                        Q(cbi__status__isnull=False) &
                        Q(cbi__status__codename="cbi:pending interview")
                        # Q(latest_cbischedule_status=True) # cbischedule.is_proceed == True
                ),
            )

            unparsed_resumes = CandidateResume.objects.filter(is_parsed=False).aggregate(count=Count('id'))
            
            metrics = {'unparsed_resumes':unparsed_resumes['count'],**metrics}
            out = {"metrics":metrics, 'statuses':statuses, 'source':lst_sources, 'category':lst_category, 'today':today, 'start_of_week':start_of_week, 'end_of_week':end_of_week,}

            # return JsonResponse(out)

            return render(request,template_name,out)

        candidates = Candidate.objects
        
        # handle table manipulation (filtering, sorting)
        
        try:
            dt_query_params = parser.parse(request.get_full_path().split('?')[1])
        except IndexError:
            dt_query_params = {}

        # return JsonResponse(dt_query_params)

        
        # individual column filtering
        if 'columns' in dt_query_params:
            for dt_column in dt_query_params['columns'].values():
                
                dt_filter_val = dt_column['search']['value']
                
                if bool(dt_filter_val):
                    dt_attr:str = dt_column['data']
                    # name, date
                    if dt_attr == 'name':
                        candidates = candidates.filter(**{f"{dt_attr}__contains":dt_filter_val})
                    elif dt_attr == 'gpt_score':
                        candidates = candidates.filter(**{f"{dt_attr}__gte":float(dt_filter_val)})
                    elif dt_attr == 'date':
                        candidates = candidates.filter(**{f"{dt_attr}__gte":datetime.strptime(dt_filter_val,'%Y-%m-%d').date()})
                    else:
                        print(dt_attr)
                        dt_attr = dt_attr.rsplit('_',1)[0]
                        # source, category
                        if dt_attr in ('source','category'):
                            candidates = candidates.filter(**{f"{dt_attr}__id":dt_filter_val})
                        # gpt_status, overall_status    
                        elif dt_attr in ('gpt_status','overall_status'):
                            candidates = candidates.filter(**{f"{dt_attr}__codename":dt_filter_val})
                        # initialscreening, prescreening, cbi,
                        else:
                            candidates = candidates.filter(**{f"{dt_attr}__status__codename":dt_filter_val})

        
        # fetch list of candidates
        
        candidates = candidates.annotate( # retrieve id of respective stages
            cbi_id=Subquery(
                CBI.objects.filter(candidate=OuterRef('pk')).values('pk')[:1]
            ),
            prescreening_id=Subquery(
                Prescreening.objects.filter(candidate=OuterRef('pk')).values('pk')[:1]
            ),
            initialscreening_id=Subquery(
                InitialScreening.objects.filter(candidate=OuterRef('pk')).values('pk')[:1]
            ),
        ).values(
            'id',
            'name',
            'date',
            'gpt_score',
            new_applicant=Case(
                When(Q(date__range=(start_of_week,today)),then=Value(True)),
                default=Value(False)
            ),
            initialscreening_id=Case(
                When(Q(initialscreening__status__isnull=False),then=F('initialscreening__id')),
                default=Value(None)
            ),
            prescreening_id=Case(
                When(Q(prescreening__status__isnull=False),then=F('prescreening__id')),
                default=Value(None)
            ),
            cbi_id=Case(
                When(Q(cbi__status__isnull=False),then=F('cbi__id')),
                default=Value(None)
            ),
            overall_status_=F('overall_status__status'),
            overall_status_codename=F('overall_status__codename'),
            category_=F('category__category'),
            source_=F('source__source'),
            gpt_status_=F('gpt_status__status'),
            initialscreening_status=Case(
                When(Q(initialscreening__status__isnull=False),then=F('initialscreening__status__status')),
                default=Value('-')
            ),
            prescreening_status=Case(
                When(Q(prescreening__status__isnull=False) & Q(prescreening__is_active=True),then=F('prescreening__status__status')),
                default=Value('-')
            ),
            cbi_status=Case(
                When(Q(cbi__status__isnull=False) & Q(cbi__is_active=True),then=F('cbi__status__status')),
                default=Value('-')
            ),
            href=Case(
                When(
                    Q(cbi__status__isnull=False),
                    then=Concat(
                        Value(reverse('main:cbi.index.default',)), F('cbi_id'), output_field=CharField(),
                    )
                ),
                When(
                    Q(prescreening__status__isnull=False),
                    then=Concat(
                        Value(reverse('main:prescreening.index.default',)), F('prescreening_id'), output_field=CharField(),
                    )
                ),
                default=Concat(
                    Value(reverse('main:initscreening.index.default')), F('initialscreening_id'), output_field=CharField(),
                )
            ),
            is_resume=Case(
                When(Q(candidate_resume__isnull=False),then=Value(True)),
                default=Value(False)
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

class BrowseRowDetailsView(CustomLoginRequired,View):

    def get(self,request:HttpRequest):

        candidate = Candidate.objects.filter(id=request.GET['candidate_id'])
        
        remarks = candidate.values(
            initialscreening_remarks=Case(
                When(Q(initialscreening__remarks__isnull=False),then=F('initialscreening__remarks')),
                default=Value('-'),
                output_field=TextField(),
            ),
            # prescreening_remarks=Case(
            #     When(Q(prescreening__remarks__isnull=False),then=F('prescreening__remarks')),
            #     default=Value('-')
            # ),
            cbi_remarks=Case(
                When(Q(cbi__remarks__isnull=False),then=F('cbi__remarks')),
                default=Value('-'),
                output_field=TextField(),
            ),
        )[0]

        details = candidate.values(
            source_ = F('source__source'),
            nationality_ = F('nationality__nationality'),
        )[0]

        return JsonResponse({'remarks':remarks,'details':details})

