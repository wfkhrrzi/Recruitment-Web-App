from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse, HttpRequest, HttpResponseBadRequest, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin

from main.views.cbi import CBICreate
from main.auth import CustomLoginRequired
from main.models import Prescreening,PrescreeningSubmission,Candidate,Status
from main.forms import PrescreeningSubmissionForm
from main.utils import return_json
from django.forms.models import model_to_dict
from django.urls import reverse
from datetime import datetime
from django.core import serializers


class PrescreeningIndex(CustomLoginRequired,View):
    
    def get(self,request,prescreening_id):
        
        prescreening_obj = Prescreening.objects.get(id=prescreening_id)

        if return_json(request):
            return JsonResponse(serializers.serialize('python',[prescreening_obj]),safe=False)

        return HttpResponse(prescreening_obj)

@method_decorator(csrf_exempt,name='dispatch')
class PrescreeningCreate(CustomLoginRequired,View):

    @classmethod
    def post(self,request:HttpRequest,):
        
        try:
            candidate = Candidate.objects.get(id=request.POST['candidate'])
        except:
            if return_json(request):
                return JsonResponse({
                    'candidate':'candidate id not found'
                })
            
            return HttpResponseBadRequest('candidate id not found')

        prescreening = Prescreening(candidate=candidate)
        prescreening.status = Status.objects.get(codename='pending')
        prescreening.assessment_status = Status.objects.get(codename='prescreening:send instruction')
        prescreening.created_by = request.user

        prescreening.save()
            
        if return_json(request):
            response = {'prescreening:create':'success'}
            
            if request.POST.get('initial_screening',None):
                response['initial_screening:update'] = 'success'                
            
            return JsonResponse(response)

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:prescreening.index',args=[prescreening.id]))


@method_decorator(csrf_exempt,name='dispatch')
class PrescreeningInstructionSent(CustomLoginRequired,View): # mail functionality coming soon

    def post(self,request:HttpRequest,):
        
        try:
            prescreening = Prescreening.objects.get(id=request.POST['prescreening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'prescreening':'prescreening id not found'
                })
            
            return HttpResponseBadRequest('prescreening id not found')

        prescreening.is_sent_instruction=True
        prescreening.instruction_date = datetime.now()
        prescreening.status = Status.objects.get(codename='prescreening:pending submission')

        prescreening.last_modified_by = request.user
        prescreening.save()
            
        if return_json(request):
            return JsonResponse({
                'prescreening:send instruction':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


@method_decorator(csrf_exempt,name='dispatch')
class PrescreeningUpdate(CustomLoginRequired,View): # mail functionality coming soon

    def post(self,request:HttpRequest,):

        if request.POST.get('proceed',None) == None:
            if return_json(request):
                return JsonResponse({
                    'proceed':'proceed is required'
                })
            
            return HttpResponseBadRequest('proceed is required')

        try:
            prescreening = Prescreening.objects.get(id=request.POST['prescreening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'prescreening':'prescreening id not found'
                })
            
            return HttpResponseBadRequest('prescreening id not found')

        if int(request.POST['proceed']) == 0: #do not proceed

            prescreening.is_proceed = False
            prescreening.status = Status.objects.get(codename='prescreening:not proceed')

        elif int(request.POST['proceed']) == 1: #proceed
            
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

        prescreening.last_modified_by = request.user
        prescreening.save()

        if prescreening.is_proceed:

            cbi_request = request
            cbi_request.POST = QueryDict(f'candidate={prescreening.candidate.id}&prescreening={True}')

            return CBICreate.post(cbi_request)
        
        else:
            if return_json(request):
                return JsonResponse({
                    'prescreening:update':'success',
                    'instance':{
                        'is_proceed':prescreening.is_proceed,
                        'status':prescreening.status,
                        'candidate':{
                            'name':prescreening.candidate.name
                        },
                    }
                })
            
            return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))

        

@method_decorator(csrf_exempt,name='dispatch')
class PrescreeningSubmissionCreate(CustomLoginRequired,View):

    def post(self,request:HttpRequest,):
        
        # check if no submission yet
        prescreening = Prescreening.objects.get(id=request.POST['prescreening'])
        prescreening_submissions = PrescreeningSubmission.objects.filter(prescreening=prescreening)
        
        files = request.FILES.getlist('submission')

        # handle submission is missing
        if files == list():
            return JsonResponse({'submission':'This field is required.'})

        for file in files:

            form = PrescreeningSubmissionForm(request.POST,dict(submission=file))
            
            if form.is_valid():                
                ps_obj:PrescreeningSubmission = form.save()
                ps_obj.created_by = request.user
                ps_obj.save()
            
            else:
                return JsonResponse(form.errors)
        
        if not prescreening_submissions:
            prescreening.status = Status.objects.get(codename='prescreening:assessment submitted')
            prescreening.save(update_fields=['status'])


        if return_json(request):
            return JsonResponse({
                'prescreening_submission':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
    

@method_decorator(csrf_exempt,name='dispatch')
class PrescreeningSubmissionDelete(CustomLoginRequired,View):
    
    def post(self,request:HttpRequest,):

        # fetch related screening submission & perform error handling
        prescreening_submission:PrescreeningSubmission = PrescreeningSubmission.objects.get(id=request.POST['prescreening_submission'])

        if prescreening_submission == None:
            if return_json(request):
                return JsonResponse({
                    'prescreening_submission':'id is not found',
                })
            
            return HttpResponseBadRequest('prescreening_submission id not found')

        prescreening_submission = prescreening_submission.delete(commit=False)
        prescreening_submission.deleted_by = request.user
        prescreening_submission.deleted_at = datetime.now()

        prescreening_submission.save()

        # reset status if no submission files
        if not PrescreeningSubmission.objects.filter(prescreening=prescreening_submission.prescreening):
            prescreening = prescreening_submission.prescreening
            prescreening.status = Status.objects.get(codename='prescreening:pending submission')
            prescreening.save(update_fields=['status'])

        if return_json(request):
            return JsonResponse({
                'prescreening_submission':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))




