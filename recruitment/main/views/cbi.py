from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse, HttpRequest, HttpResponseBadRequest, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from main.auth import CustomLoginRequired
from main.models import CBI,CBISubmission,Candidate,Status, CBISchedule
from main.forms import CBIScheduleForm
from main.utils import return_json
from django.forms.models import model_to_dict
from django.urls import reverse
from datetime import datetime
from django.core import serializers

from main.forms import CBISubmissionForm

class CBIIndex(CustomLoginRequired,View):
    
    def get(self,request,cbi_id):
        
        cbi_obj = CBI.objects.get(id=cbi_id)

        if return_json(request):
            return JsonResponse(serializers.serialize('python',[cbi_obj]),safe=False)
            # return JsonResponse({'view':True})

        return HttpResponse(cbi_obj)

@method_decorator(csrf_exempt,name='dispatch')
class CBICreate(CustomLoginRequired,View):

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

        prescreening = CBI(candidate=candidate)
        prescreening.status = Status.objects.get(codename='cbi:unscheduled')
        prescreening.created_by = request.user

        prescreening.save()
            
        if return_json(request):
            response = {'cbi:create':'success'}
            
            if request.POST.get('prescreening',None):
                response['prescreening:update'] = 'success'                
            
            return JsonResponse(response)

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:cbi.index',args=[prescreening.id]))


@method_decorator(csrf_exempt,name='dispatch')
class CBIScheduleCreate(CustomLoginRequired,View): # mail functionality coming soon

    @classmethod
    def post(self,request:HttpRequest,):
        
        try:
            cbi = CBI.objects.get(id=request.POST['cbi'])
        except:
            if return_json(request):
                return JsonResponse({
                    'cbi':'cbi id not found'
                })
            
            return HttpResponseBadRequest('cbi id not found')

        form = CBIScheduleForm(request.POST)

        if not form.is_valid():
            return JsonResponse(form.errors)
            
        cbischedule:CBISchedule = form.save(commit=False)
        cbischedule.status = Status.objects.get(codename='cbi_schedule:pending send RSVP')
        cbischedule.cbi = cbi
        
        if request.POST.get('cbi_reschedule',None): # return model instance to CBIReschedule
            return 
        
        cbischedule.save()
        
        if return_json(request):
            return JsonResponse({
                'cbi-schedule:create':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


@method_decorator(csrf_exempt,name='dispatch')
class CBIScheduleUpdate(CustomLoginRequired,View): # mail functionality coming soon

    def post(self,request:HttpRequest,):
        
        try:
            cbischedule = CBISchedule.objects.get(id=request.POST['cbi_schedule'])
        except:
            if return_json(request):
                return JsonResponse({
                    'cbi_schedule':'cbi_schedule id not found'
                })
            
            return HttpResponseBadRequest('cbi_schedule id not found')
        
        before_data = serializers.serialize('python',[cbischedule])

        form = CBIScheduleForm(request.POST,instance=cbischedule) # handle all validations
        if form.is_valid():
            
            cbischedule = form.save()
            
            if return_json(request):
                return JsonResponse({
                    'cbi-schedule:edit':'success',
                    'before':before_data,
                    'after':serializers.serialize('python',[cbischedule]),
                })

            return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))

        return JsonResponse(form.errors)


@method_decorator(csrf_exempt,name='dispatch')
class CBIScheduleSendRSVP(CustomLoginRequired,View): # mail functionality coming soon

    def post(self,request:HttpRequest,):
        
        try:
            cbischedule = CBISchedule.objects.get(id=request.POST['cbi_schedule'])
        except:
            if return_json(request):
                return JsonResponse({
                    'cbi_schedule':'cbi_schedule id not found'
                })
            
            return HttpResponseBadRequest('cbi_schedule id not found')
        
        # processes to send RSVP to respective assessors via Outlook

        cbischedule.is_RSVP = True
        cbischedule.status = Status.objects.get(codename='cbi_schedule:pending RSVP response')
            
        if return_json(request):
            return JsonResponse({
                'cbi-schedule:send RSVP':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


class CBIScheduleGetRSVP(CustomLoginRequired,View):
    ''' Receive RSVP from involved assessors via Outlook '''
    pass


@method_decorator(csrf_exempt,name='dispatch')
class CBIReschedule(CustomLoginRequired,View): # mail functionality coming soon

    def post(self,request:HttpRequest,):
        
        new_POST = QueryDict(f'cbi_reschedule={True}',mutable=True)
        new_POST.update(request.POST)
        request.POST = new_POST

        response = CBIScheduleCreate.post(request)

        if not response:
            return response
        
        old_cbischedule = CBISchedule.objects.filter(is_proceed=True).first()
        old_cbischedule.is_proceed = False
        old_cbischedule.save()

            
        if return_json(request):
            return JsonResponse({
                'cbi-reschedule':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


@method_decorator(csrf_exempt,name='dispatch')
class CBIUpdate(CustomLoginRequired,View): # mail functionality coming soon

    def post(self,request:HttpRequest,):

        if request.POST.get('proceed',None) == None:
            if return_json(request):
                return JsonResponse({
                    'proceed':'proceed is required'
                })
            
            return HttpResponseBadRequest('proceed is required')

        try:
            prescreening = CBI.objects.get(id=request.POST['prescreening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'prescreening':'prescreening id not found'
                })
            
            return HttpResponseBadRequest('prescreening id not found')

        if int(request.POST['proceed']) == 0: #do not proceed

            prescreening.is_proceed = False
            prescreening.status = Status.objects.get(codename='do not proceed')

        elif int(request.POST['proceed']) == 1: #proceed
            
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='proceed')

        prescreening.last_modified_by = request.user
        prescreening.save()
            
        if return_json(request):
            return JsonResponse({
                'prescreening:update':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
        

@method_decorator(csrf_exempt,name='dispatch')
class CBISubmissionCreate(CustomLoginRequired,View):

    def post(self,request:HttpRequest,):
        
        # check if no submission yet
        prescreening = CBI.objects.get(id=request.POST['prescreening'])
        prescreening_submissions = CBISubmission.objects.filter(prescreening=prescreening)
        
        files = request.FILES.getlist('submission')

        # handle submission is missing
        if files == list():
            return JsonResponse({'submission':'This field is required.'})

        for file in files:

            form = CBISubmissionForm(request.POST,dict(submission=file))
            
            if form.is_valid():                
                ps_obj:CBISubmission = form.save()
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
class CBISubmissionDelete(CustomLoginRequired,View):
    
    def post(self,request:HttpRequest,):

        # fetch related screening submission & perform error handling
        prescreening_submission:CBISubmission = CBISubmission.objects.get(id=request.POST['prescreening_submission'])

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
        if not CBISubmission.objects.filter(prescreening=prescreening_submission.prescreening):
            prescreening = prescreening_submission.prescreening
            prescreening.status = Status.objects.get(codename='prescreening:pending submission')
            prescreening.save(update_fields=['status'])

        if return_json(request):
            return JsonResponse({
                'prescreening_submission':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))




