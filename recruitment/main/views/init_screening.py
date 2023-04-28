from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse, HttpRequest, HttpResponseBadRequest, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from main.auth import CustomLoginRequired
from main.models import InitialScreening,Status,Candidate,Users, InitialScreeningEvaluation
from main.forms import InitialScreeningCreateForm, PrescreeningSubmissionForm
from main.utils import return_json
from main.views.pre_screening import PrescreeningCreate
from django.forms.models import model_to_dict
from django.urls import reverse
from datetime import datetime
from django.core import serializers


class InitialScreeningIndex(CustomLoginRequired,View):
    
    def get(self,request,initial_screening_id):
        
        prescreening_obj = InitialScreening.objects.get(id=initial_screening_id)

        if return_json(request):
            return JsonResponse(serializers.serialize('python',[prescreening_obj]),safe=False)

        return HttpResponse(prescreening_obj)


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

        intial_screening = InitialScreening.objects.create(candidate=candidate,selection_status=Status.objects.get(codename='initscreening:pending'))
                    
        if return_json(request):
            return JsonResponse({
                'initial_screening':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))

@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningEvaluationCreate(CustomLoginRequired,View): # create & update

    def post(self,request: HttpRequest):

        if request.POST.get('proceed',None) == None:
            if return_json(request):
                return JsonResponse({
                    'proceed':'proceed is required'
                })
            
            return HttpResponseBadRequest('proceed is required')

        try:
            initial_screening = InitialScreening.objects.get(id=request.POST['initial_screening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'initial_screening':'initial_screening not found'
                })
            
            return HttpResponseBadRequest('initial_screening not found')
        
        try:
            user = Users.objects.get(id=request.POST['user'])
        except:
            if return_json(request):
                return JsonResponse({
                    'user':'user not found'
                })
            
            return HttpResponseBadRequest('user not found')

        try:
            initial_screening_eval = InitialScreeningEvaluation.objects.get(initial_screening=initial_screening,user=user)
        except: 
            initial_screening_eval = InitialScreeningEvaluation(initial_screening=initial_screening,user=user,created_by=request.user)
        
        if int(request.POST['proceed']) == 0: #do not proceed
            initial_screening_eval.is_proceed = False
            initial_screening_eval.status = Status.objects.get(codename='rejected')

        elif int(request.POST['proceed']) == 1: #proceed
            
            initial_screening_eval.is_proceed = True
            initial_screening_eval.status = Status.objects.get(codename='proceed')

        initial_screening_eval.save()

        if return_json(request):
            return JsonResponse({
                'initial_screening_eval':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


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

        if return_json(request):
            return JsonResponse({
                'initial_screening_eval':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


class InitialScreeningEdit(CustomLoginRequired,View):

    def get(self,request: HttpRequest):
        return HttpResponse('return http page')


@method_decorator(csrf_exempt,name='dispatch')
class InitialScreeningUpdate(CustomLoginRequired,View):
    
    def post(self,request: HttpRequest,):
        ''' 
        Update Initial Screening's is_proceed & selection_status
        
        :return InitialScreening
         
        '''

        # error handling
        if request.POST.get('proceed',None) == None:
            if return_json(request):
                return JsonResponse({
                    'proceed':'proceed is required'
                })
            
            return HttpResponseBadRequest('proceed is required')

        try:
            initial_screening = InitialScreening.objects.get(id=request.POST['initial_screening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'initial_screening':'initial_screening not found'
                })
            
            return HttpResponseBadRequest('initial_screening not found')
        
        if int(request.POST['proceed']) == 0: #do not proceed
            initial_screening.is_proceed = False
            initial_screening.selection_status = Status.objects.get(codename='initscreening:not selected')

        elif int(request.POST['proceed']) == 1: #proceed
            
            initial_screening.is_proceed = True
            initial_screening.selection_status = Status.objects.get(codename='initscreening:selected')
            initial_screening.selection_date = datetime.now()
        
        initial_screening.last_modified_by = request.user
        initial_screening.save()


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
                        'selection_status':initial_screening.selection_status.status,
                        'candidate':{
                            'name':initial_screening.candidate.name
                        },
                    }
                })
            
            return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))

