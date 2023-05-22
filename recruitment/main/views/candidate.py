from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from main.auth import CustomLoginRequired
from main.utils import return_json
from main.models import Candidate, CandidateResume
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from main.forms import ResumeSubmissionForm
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CandidateIndex(CustomLoginRequired,View):

    def get(self,request:HttpRequest):
        
        page_size = request.GET.get('page_size') or 10 # default to 10
        page_number = request.GET.get('page') or 1 # default to 10
        
        candidates = Candidate.objects.all()
        paginator = Paginator(candidates,page_size)
        page_obj = paginator.get_page(page_number)
        lst_candidates = serializers.serialize('python',page_obj) # serialize the queryset contained from get_page()
        
        data = {
            "page":{
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
                'number_of_pages': paginator.num_pages,
                'count': paginator.count,            
            },

            "candidates":lst_candidates,

        }

        if return_json(request):
            return JsonResponse(data)
            
        return HttpResponse(f'candidate index page (table)\n\n {data}')


class CandidateEdit(CustomLoginRequired,UserPassesTestMixin,View):

    def get(self,request):
        return HttpResponse('candidate edit page')


class CandidateUpdate(UserPassesTestMixin,View):
    
    def post(self,request):
        pass

@method_decorator(csrf_exempt,name='dispatch')
class CandidateResumeCreate(CustomLoginRequired,View):

    def post(self,request:HttpRequest):

        files = request.FILES.getlist('submission') or request.FILES.getlist('submission[]') or None

        # return JsonResponse({'POST':request.POST,'FILES':request.FILES.get('submission').name})
        
        # handle missing submission
        if files == None:
            response = JsonResponse({'submission':'submission are required'})
            response.status_code = 400
            return response
        
        form_errors = dict()

        for file in files:

            ps_obj:CandidateResume = CandidateResume(submission=file)
            ps_obj.created_by = request.user
            ps_obj.save()

            # form = ResumeSubmissionForm(request.POST,dict(submission=file))
            
            # if form.is_valid():                
            #     ps_obj:CandidateResume = form.save(commit=False)
            #     ps_obj.created_by = request.user
            #     ps_obj.save()
            
            # else:
            #     form_errors[file] = form.errors.as_data()


        if return_json(request):
            return JsonResponse({
                'prescreening_submission':'success',
                'errors':form_errors,
            })

        return redirect(request.META.get('HTTP_REFERER') or reverse('main:candidate.index'))