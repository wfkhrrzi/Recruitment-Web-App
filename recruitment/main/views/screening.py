from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from ..auth import CustomLoginRequired
from ..models import Screening,ScreeningSubmission
from ..forms import ScreeningForm, ScreeningSubmissionForm
from ..utils import return_json
from django.forms.models import model_to_dict
from django.urls import reverse

@method_decorator(csrf_exempt,name='dispatch')
class ScreeningCreate(CustomLoginRequired,View):

    def get(self,request:HttpRequest):
        return HttpResponse('screening page')

    def post(self,request: HttpRequest):
        form = ScreeningForm(request.POST)
        if form.is_valid():
                
            form.save()
            
            if return_json(request):
                return JsonResponse({
                    'response':'success',
                })

            return redirect(request.META.get('HTTP_REFERER'),reverse('main:candidate.index'))
        
        return HttpResponse('Form not valid')
   
class ScreeningEdit(CustomLoginRequired,View):

    def get(self,request: HttpRequest):
        return HttpResponse('return http page')

@method_decorator(csrf_exempt,name='dispatch')
class ScreeningUpdate(CustomLoginRequired,View):
    
    def post(self,request: HttpRequest, form_class=ScreeningForm):
        try:
            screening = Screening.objects.get(id=request.POST['screening'])
        except:
            if return_json(request):
                return JsonResponse({
                    'response':'error',
                    'error':'screening not found'
                })
            
            return HttpResponseBadRequest('screening not found')
        
        form = form_class(request.POST,instance=screening)
        
        if form.is_valid():
            
            form.save()

            if return_json(request):
                return JsonResponse({
                    'response':'success',
                })

            return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
        
        return HttpResponse('Form not valid')

@method_decorator(csrf_exempt,name='dispatch')
class ScreeningSubmissionCreate(CustomLoginRequired,View):

    def post(self,request:HttpRequest,form_class=ScreeningSubmissionForm):

        form = form_class(request.POST,request.FILES)
        
        if form.is_valid():
            
            form.save()

            if return_json(request):
                return JsonResponse({
                    'response':'success',
                })

            return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
        
        return JsonResponse(form.errors)

@method_decorator(csrf_exempt,name='dispatch')
class ScreeningSubmissionDelete(CustomLoginRequired,View):

    
    def post(self,request:HttpRequest,form_class=ScreeningSubmissionForm):
        
        # fetch related screening submission & perform error handling
        screening_submission:ScreeningSubmission = ScreeningSubmission.objects.filter(id=request.POST['screening_submission']).first()
        
        if screening_submission == None:
            if return_json(request):
                return JsonResponse({
                    'response':'error',
                    'error':'screening submission not found'
                })
            
            return HttpResponseBadRequest('screening submission not found')

        # form validation
        form = form_class(request.POST,request.FILES,instance=screening_submission,request=request)

        if form.is_valid():

            screening_submission.delete()

            if return_json(request):
                return JsonResponse({
                    'response':'success',
                })

            return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))
        
        return JsonResponse(form.errors)




