from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from ..auth import CustomLoginRequired
from main.utils import return_json
from main.models import Candidate
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers


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


class CandidateUpdate(View,UserPassesTestMixin):
    
    def post(self,request):
        pass

