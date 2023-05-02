from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.views import View
from main.models import Candidate, CBISchedule
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from main.auth import CustomLoginRequired
from main.utils import return_json
from django.db.models import Q, Case, When, CharField, Value, Count, OuterRef, Subquery
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def index(request):
    return JsonResponse('Hello world',safe=False)


class Browse(CustomLoginRequired, View):

    def get(self,request:HttpRequest):

        page_size = request.GET.get('page_size') or 10 # default to 10
        page_number = request.GET.get('page') or 1 # default to 10
        
        # fetch list of candidates
        candidates = Candidate.objects.filter(
            initialscreening__selection_status__isnull=False
        ).annotate(
            overall_status=Case(
                When(Q(cbi__status__isnull=False),then=Value("ongoing cbi")),
                When(Q(prescreening__status__isnull=False),then=Value("ongoing prescreening")),
                When(Q(initialscreening__selection_status__isnull=False),then=Value("ongoing initial screening")),
                default=None,
                output_field=CharField()
            )
        ).values(
            'name','date','source__source','gpt_status__status','initialscreening__selection_status__status','prescreening__status__status','cbi__status__status','overall_status'
        )

        # fetch action metrics
        latest_cbischedule_status = CBISchedule.objects.filter(cbi__candidate=OuterRef('pk')).order_by('-created_at').values('status__codename')[:1]
        metrics = Candidate.objects.annotate(
            latest_cbischedule_status = Subquery(latest_cbischedule_status)
        ).aggregate(
            pending_initial_screening=Count(
                'id',
                filter=
                    Q(initialscreening__selection_status__isnull=False) & 
                    ~Q(initialscreening__selection_status__codename="proceed") & 
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
        )

        paginator = Paginator(candidates,page_size)
        page_obj = paginator.get_page(page_number)
        lst_candidates = list(page_obj.object_list)
        


        data = {
            "page":{
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
                'number_of_pages': paginator.num_pages,
                'count': paginator.count,            
            },
            "metrics":metrics,
            "items":lst_candidates,

        }

        if return_json(request):
            return JsonResponse(data)
            
        return HttpResponse(f'browse page (table)\n\n {data}')