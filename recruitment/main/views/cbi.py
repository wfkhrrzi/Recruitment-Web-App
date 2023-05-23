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
from django.db.models import Q, Case, When, CharField, Value, Count, OuterRef, Subquery, F

from main.forms import CBISubmissionForm

class CBIIndex(CustomLoginRequired,View):
    
    def get(self,request,cbi_id):
        
        cbi = CBI.objects.get(id=cbi_id)

        if return_json(request):
            return JsonResponse(serializers.serialize('python',[cbi]),safe=False)
            # return JsonResponse({'view':True})

        context = {
            'cbi':serializers.serialize('python',[cbi])[0],
            'candidate':serializers.serialize('python',[cbi.candidate])[0],
        }

        return render(request,'main/pages/cbi.html',context)

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
        
        try:
            if(CBI.objects.get(candidate_id=request.POST['candidate'])):
                if return_json(request):
                    response = {
                        'CBI':f'already created for candidate_id = {request.POST["candidate"]}'
                    }
                    
                    if request.POST.get('initial_screening',None):
                        response['initial_screening:update'] = 'success'    
                    
                    return JsonResponse(response)
            
                return HttpResponse(response)
        except:
            pass

        cbi = CBI(candidate=candidate)
        cbi.status = Status.objects.get(codename='cbi:pending schedule') # change status to 'cbi:pending schedule'
        cbi.created_by = request.user

        cbi.save()
        
        candidate.overall_status = Status.objects.get(codename='cbi:ongoing')
        candidate.save()

        if return_json(request):
            response = {'cbi:create':'success'}
            
            if request.POST.get('prescreening',None):
                response['prescreening:update'] = 'success'                
            
            return JsonResponse(response)

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:cbi.index',args=[cbi.id]))


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
        
        # if request.POST.get('cbi_reschedule',None): # return model instance to CBIReschedule
        #     return 
        
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
        cbischedule.status = Status.objects.get(codename='cbi:proceed')
            
        if return_json(request):
            return JsonResponse({
                'cbi-schedule:send RSVP':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


class CBIScheduleGetRSVP(CustomLoginRequired,View):
    ''' Receive RSVP from involved assessors via Outlook '''
    def post(self,request:HttpRequest,):
        
        if request.POST.get('rsvp',None) == None:
            if return_json(request):
                return JsonResponse({
                    'rsvp':'rsvp is required'
                })
            
            return HttpResponseBadRequest('rsvp is required')

        try:
            cbischedule = CBISchedule.objects.get(id=request.POST['cbi_schedule'])
        except:
            if return_json(request):
                return JsonResponse({
                    'cbi_schedule':'cbi_schedule id not found'
                })
            
            return HttpResponseBadRequest('cbi_schedule id not found')
        
        # processes to send RSVP to respective assessors via Outlook

        if bool(int(request.POST['rsvp'])):
            cbischedule.is_RSVP = True
                
        if return_json(request):
            return JsonResponse({
                'cbi-schedule:send RSVP':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))


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

        # error handling
        if not bool(request.POST):
            response = JsonResponse({'error':'no data is passed!'})
            response.status_code = 400
            return response

        if request.POST.get('proceed',None) == None:
            is_proceed = None
            # if return_json(request):
            #     response = JsonResponse({'proceed':'proceed is required'})
            #     response.status_code = 400
            #     return response
            
            # return HttpResponseBadRequest('proceed is required')
        else:
            is_proceed = request.POST.get('proceed')

        try:
            cbi = CBI.objects.get(id=request.POST['cbi'])
        except:
            if return_json(request):
                response = JsonResponse({'cbi':'cbi id not found'})
                response.status_code = 400
                return response
            
            return HttpResponseBadRequest('cbi id not found')

        if is_proceed != None:
            if int(request.POST['proceed']) == 0: #do not proceed

                cbi.is_proceed = False
                cbi.status = Status.objects.get(codename='cbi:not proceed')

            elif int(request.POST['proceed']) == 1: #proceed
                
                cbi.is_proceed = True
                cbi.status = Status.objects.get(codename='cbi:proceed')

            elif int(request.POST['proceed']) == 2: #pending schedule
                
                cbi.status = Status.objects.get(codename='cbi:pending schedule')

            elif int(request.POST['proceed']) == 3: #pending interview
                
                cbi.status = Status.objects.get(codename='cbi:pending interview')

            elif int(request.POST['proceed']) == 4: #pending result
                
                cbi.status = Status.objects.get(codename='cbi:pending result')

        # update remarks
        if request.POST.get('remarks',None) != None:
            cbi.remarks = request.POST.get('remarks')

        cbi.last_modified_by = request.user
        cbi.save()
            
        if return_json(request):
            return JsonResponse({
                'cbi:update':'success',
                'instance':{
                    'is_proceed':cbi.is_proceed,
                    'status':cbi.status.status,
                    'remarks':cbi.remarks,
                    'candidate':{
                        'name':cbi.candidate.name
                    },
                }
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
        

@method_decorator(csrf_exempt,name='dispatch')
class CBISubmissionCreate(CustomLoginRequired,View):

    def post(self,request:HttpRequest,):
        
        # check if no submission yet
        cbi = CBI.objects.get(id=request.POST['cbi'])
        cbi_submissions = CBISubmission.objects.filter(cbi=cbi)
        
        files = request.FILES.getlist('submission')

        # handle submission is missing
        if files == list():
            return JsonResponse({'submission':'This field is required.'})

        for file in files:

            form = CBISubmissionForm(request.POST,dict(submission=file))
            
            if form.is_valid():                
                cbi_obj:CBISubmission = form.save()
                cbi_obj.created_by = request.user
                cbi_obj.save()
            
            else:
                return JsonResponse(form.errors)
        
        if not cbi_submissions:
            cbi.status = Status.objects.get(codename='cbi:assessment submitted')
            cbi.save(update_fields=['status'])


        if return_json(request):
            return JsonResponse({
                'cbi_submission':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
    

@method_decorator(csrf_exempt,name='dispatch')
class CBISubmissionDelete(CustomLoginRequired,View):
    
    def post(self,request:HttpRequest,):

        # fetch related screening submission & perform error handling
        cbi_submission:CBISubmission = CBISubmission.objects.get(id=request.POST['cbi_submission'])

        if cbi_submission == None:
            if return_json(request):
                return JsonResponse({
                    'cbi_submission':'id is not found',
                })
            
            return HttpResponseBadRequest('cbi_submission id not found')

        cbi_submission = cbi_submission.delete(commit=False)
        cbi_submission.deleted_by = request.user
        cbi_submission.deleted_at = datetime.now()

        cbi_submission.save()

        # reset status if no submission files
        if not CBISubmission.objects.filter(cbi=cbi_submission.cbi):
            cbi = cbi_submission.cbi
            cbi.status = Status.objects.get(codename='cbi:pending submission')
            cbi.save(update_fields=['status'])

        if return_json(request):
            return JsonResponse({
                'cbi_submission':'success',
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))




