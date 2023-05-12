from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse, HttpRequest, HttpResponseBadRequest, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from main.auth import CustomLoginRequired
from main.models import InitialScreening,Status,Candidate,Users, InitialScreeningEvaluation
from main.forms import InitialScreeningCreateForm, PrescreeningSubmissionForm
from main.utils import return_json, extract_candidate_info
from main.views.pre_screening import PrescreeningCreate
from django.forms.models import model_to_dict
from django.urls import reverse
from datetime import datetime
from django.core import serializers
from django.db.models import Q, Case, When, Value, Count, OuterRef, Subquery, F, CharField, JSONField
from django.db.models.functions import Concat, Cast
from django.template.loader import render_to_string

def get_lst_ds_leads(initial_screening:InitialScreening,is_evaluated:bool="none") -> list:

    if is_evaluated == "none":
        eval_is_proceed_filter_kwarg = {}
    else:
        eval_is_proceed_filter_kwarg = {'eval_is_proceed':is_evaluated}

    ds_leads = Users.objects.filter(
        user_category__category__iexact='ds lead',
    ).annotate(
        full_name=Concat(F('first_name'),Value(' '),F('last_name'),output_field=CharField()),
        eval_id=Subquery(
            InitialScreeningEvaluation.objects.filter(
                initial_screening=initial_screening,
                user=OuterRef('pk')
            ).values('id')[:1]
        ),
        eval_is_proceed=Subquery(
            InitialScreeningEvaluation.objects.filter(
                initial_screening=initial_screening,
                user=OuterRef('pk')
            ).values('is_proceed')[:1]
        ),
        eval_status=Subquery(
            InitialScreeningEvaluation.objects.filter(
                initial_screening=initial_screening,
                user=OuterRef('pk')
            ).values('status__status')[:1]
        ),
    ).filter(
        **eval_is_proceed_filter_kwarg
    ).values(
        'id',
        'full_name',
        'alias',
        'eval_id',
        'eval_is_proceed',
        'eval_status',
    )

    return list(ds_leads)

def output_json_ds_leads(initial_screening:InitialScreening) -> dict:
    out = {
        "none":list(),
        "true":list(),
        "false":list(),
    }
    
    for lead in get_lst_ds_leads(initial_screening, None):
        out['none'].append(
            render_to_string('main/components/initscreening/label_leads.html', {'lead':lead})
        )
    
    for lead in get_lst_ds_leads(initial_screening, True):
        out['true'].append(
            render_to_string('main/components/initscreening/eval_label_leads.html', {'lead':lead})
        )
    
    for lead in get_lst_ds_leads(initial_screening, False):
        out['false'].append(
            render_to_string('main/components/initscreening/eval_label_leads.html', {'lead':lead})
        )

    return out


class InitialScreeningIndex(CustomLoginRequired,View):
    
    def get(self,request:HttpRequest,initial_screening_id=None):
        
        initial_screening = InitialScreening.objects.filter(id=initial_screening_id).values(
            'pk',
            "last_modified_at",
            "is_hm_proceed",
            "hm_date_selected",
            "date_selected",
            "is_proceed",
            "remarks",
            hm_status_ = F("hm_status__status"),
            status_ = F("status__status"),
            last_modified_by_ = Concat(
                F("last_modified_by__first_name"),Value(' '),F("last_modified_by__last_name"),
                Value(' ('),F("last_modified_by__alias"),Value(')')
            ),
        )

        candidate = extract_candidate_info(InitialScreening.objects.get(id=initial_screening_id))
        ds_leads = get_lst_ds_leads(InitialScreening.objects.get(id=initial_screening_id))

        context = {
            'initial_screening':list(initial_screening)[0],
            'candidate':candidate,
            'ds_leads':ds_leads,
        }

        if return_json(request):
            return JsonResponse(context,safe=False)

        return render(request,'main/pages/initscreening.html',context)


@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningCreate(CustomLoginRequired,View):

    def get(self,request:HttpRequest):
        return HttpResponse('initial screening page')

    def post(self,request: HttpRequest):

        try:
            candidate = Candidate.objects.get(id=request.POST['candidate'])
        except:
            if return_json(request):
                return JsonResponse({
                    'candidate':'candidate not found'
                })
            
            return HttpResponseBadRequest('candidate not found')

        intial_screening = InitialScreening.objects.create(candidate=candidate,status=Status.objects.get(codename='initscreening:pending'))
                    
        if return_json(request):
            return JsonResponse({
                'initial_screening':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningHiringUpdate(CustomLoginRequired,View):
    
    def post(self,request: HttpRequest,):
        ''' 
        Update Initial Screening's is_proceed & status
        
        :return InitialScreening
         
        '''

        # error handling
        if not bool(request.POST):
            response = JsonResponse({'error':'no data is passed!'})
            response.status_code = 400
            return response

        if request.POST.get('proceed',None) == None:
            is_proceed = None
            if return_json(request):
                response = JsonResponse({'proceed':'proceed is required'})
                response.status_code = 400
                return response
            
            return HttpResponseBadRequest('proceed is required')
        else:
            is_proceed = request.POST.get('proceed')

        try:
            initial_screening = InitialScreening.objects.get(id=request.POST['initial_screening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'initial_screening':'initial_screening not found'
                })
            
            return HttpResponseBadRequest('initial_screening not found')
        
        if is_proceed != None:
            if int(is_proceed) == 0: #do not proceed
                initial_screening.is_hm_proceed = False
                initial_screening.hm_status = Status.objects.get(codename='initscreening:not selected')

            elif int(is_proceed) == 1: #proceed
                
                initial_screening.is_hm_proceed = True
                initial_screening.hm_status = Status.objects.get(codename='initscreening:selected')
                initial_screening.hm_date_selected = datetime.now()

        initial_screening.last_modified_by = request.user
        initial_screening.save()

        # proceed to ds leads screening OR return output
        out = {
            'update':'success',
            'hm_screening':{
                'is_hm_proceed':initial_screening.is_hm_proceed,
                'hm_status':initial_screening.hm_status.status,
                'hm_date_selected':initial_screening.hm_date_selected,
            }
        }

        if return_json(request):
            return JsonResponse(out)
        
        return redirect(
            # request.META.get('HTTP_REFERER') or 
            reverse('main:initscreening.index',args=[initial_screening.id])
        )


@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningEvaluationCreate(CustomLoginRequired,View): # create & update

    def post(self,request: HttpRequest):

        lst_users = request.POST.getlist('users') or request.POST.getlist('users[]') or None
        
        if lst_users == None:
            response = JsonResponse({'users':'users are required'})
            response.status_code = 400
            return response

        if request.POST.get('proceed',None) == None:
            if return_json(request):
                response = JsonResponse({'proceed':'proceed is required'})
                response.status_code = 400
                return response
            
            return HttpResponseBadRequest('proceed is required')

        try:
            initial_screening = InitialScreening.objects.get(id=request.POST['initial_screening'])
        except:
            if return_json(request):
                response = JsonResponse({'initial_screening':'initial_screening not found'})
                response.status_code = 400
                return response
            
            return HttpResponseBadRequest('initial_screening not found')
        
        
        users = Users.objects.filter(id__in=lst_users) # no error handling

        
        if int(request.POST['proceed']) == 0: #do not proceed
            final_is_proceed = False
            final_status = Status.objects.get(codename='initscreening:not proceed')

        elif int(request.POST['proceed']) == 1: #proceed
            
            final_is_proceed = True
            final_status = Status.objects.get(codename='initscreening:proceed')

        for user in users:
            InitialScreeningEvaluation.objects.update_or_create(
                initial_screening=initial_screening,
                user=user,
                defaults={
                    'status':final_status,
                    'is_proceed':final_is_proceed,
                }
            )

        # return JsonResponse({
        #     'ds_leads':get_lst_ds_leads(initial_screening),
        # })

        # return ajax response

        out = output_json_ds_leads(initial_screening)

        return JsonResponse(out)


@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningEvaluationDelete(CustomLoginRequired,View): # create & update

    def post(self,request: HttpRequest):

        try:
            initial_screening_eval = InitialScreeningEvaluation.objects.get(id=request.POST['initial_screening_eval'])
        except:
            if return_json(request):
                return JsonResponse({
                    'initial_screening_eval':'initial_screening_eval not found'
                })
            
            return HttpResponseBadRequest('initial_screening_eval not found')

        initial_screening_eval.is_proceed = None
        initial_screening_eval.status = None
        initial_screening_eval.last_modified_by = request.user

        initial_screening_eval.save()

        out = output_json_ds_leads(initial_screening_eval.initial_screening)

        return JsonResponse(out)

        # if return_json(request):
        #     return JsonResponse({
        #         'initial_screening_eval':'success',
        #     })

        # return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


class InitialScreeningEdit(CustomLoginRequired,View):

    def get(self,request: HttpRequest):
        return HttpResponse('return http page')


@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningUpdate(CustomLoginRequired,View):
    
    def post(self,request: HttpRequest,):
        ''' 
        Update Initial Screening's is_proceed & status
        
        :return InitialScreening
         
        '''

        # error handling
        if not bool(request.POST):
            response = JsonResponse({'error':'no data is passed!'})
            response.status_code = 400
            return response

        if request.POST.get('proceed',None) == None:
            is_proceed = None
            # if return_json(request):
            #     return JsonResponse({
            #         'proceed':'proceed is required'
            #     })
            
            # return HttpResponseBadRequest('proceed is required')
        else:
            is_proceed = request.POST.get('proceed')

        try:
            initial_screening = InitialScreening.objects.get(id=request.POST['initial_screening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'initial_screening':'initial_screening not found'
                })
            
            return HttpResponseBadRequest('initial_screening not found')
        
        if is_proceed != None:
            if int(is_proceed) == 0: #do not proceed
                initial_screening.is_proceed = False
                initial_screening.status = Status.objects.get(codename='initscreening:not selected')

            elif int(is_proceed) == 1: #proceed
                
                initial_screening.is_proceed = True
                initial_screening.status = Status.objects.get(codename='initscreening:selected')
                initial_screening.date_selected = datetime.now()
        
        # update remarks
        if request.POST.get('remarks',None) != None:
            initial_screening.remarks = request.POST.get('remarks')

        initial_screening.last_modified_by = request.user
        initial_screening.save()

        # proceed to next stage OR return output
        if initial_screening.is_proceed:
            prescreening_request = request
            prescreening_request.POST = QueryDict(f'candidate={initial_screening.candidate.id}&initial_screening={True}')

            return PrescreeningCreate.post(prescreening_request)
        
        else:
            if return_json(request):
                return JsonResponse({
                    'initial_screening:update':'success',
                    'instance':{
                        'is_proceed':initial_screening.is_proceed,
                        'status':initial_screening.status.status,
                        'candidate':{
                            'name':initial_screening.candidate.name
                        },
                    }
                })
            
            return redirect(
                # request.META.get('HTTP_REFERER') or 
                reverse('main:initscreening.index',args=[initial_screening.id])
            )

