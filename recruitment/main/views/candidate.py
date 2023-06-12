from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpRequest,FileResponse
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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from main.tasks import parse_resumes
from django_eventstream import send_event
from main.utils import get_active_tasks
import json
from django_celery_results.models import TaskResult
from io import BytesIO


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

class CandidateResumeOpen(CustomLoginRequired,View):

    def get(self,request:HttpRequest,candidate_id):

        resume = CandidateResume.objects.get(candidate=Candidate.objects.get(id=candidate_id))
        response = FileResponse(BytesIO(resume.submission),content_type='application/pdf')
        # response['Content-Disposition'] = 'inline; filename="file.pdf"'

        return response


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

            ps_obj:CandidateResume = CandidateResume(filename=file.name)

            # Read the uploaded file and store it as binary data in the model's BinaryField
            with BytesIO() as buffer:
                for chunk in file.chunks():
                    buffer.write(chunk)
                ps_obj.submission = buffer.getvalue()
            
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


class CandidateResumeRead(CustomLoginRequired,View):

    def get(self,request:HttpRequest):

        rawResumes = CandidateResume.objects.filter(is_parsed=False,is_parsing=False)
        candidateResumes = rawResumes.all()
        countResumes = rawResumes.aggregate(
            count=Count(
                'id',
                filter=Q(is_parsed=False),
            )
        ) 

        return JsonResponse({
            'data':serializers.serialize('python',candidateResumes),
            'count':countResumes['count'],
        })

@method_decorator(csrf_exempt,name='dispatch')
class CandidateResumeParse(CustomLoginRequired,View):

    def post(self,request:HttpRequest):

        for i in ('job_title','job-description',):
            if request.POST.get(i, None) == None:
                response = JsonResponse({'job_title':'job_title are required'})
                response.status_code = 400
                return response
        
        # initialize resume object (for parsing process & tracking parsing progress)
        resumes_obj = CandidateResume.objects.filter(is_parsed=False,is_parsing=False)

        if resumes_obj.exists():
            
            # execute parsing in job queues 
            task = parse_resumes.apply_async(
                args=(
                    request.POST['job_title'],
                    request.POST['job-description'],
                    serializers.serialize('json',resumes_obj),
                    request.user.id
                )
            )

            # set is_parsing = True
            resumes_obj.update(is_parsing=True)

            metric = resumes_obj.aggregate(
                total=Count('id')
            )

            # send notification to the clients via SSE
            # tasks = TaskResult.objects.filter(status__in=['STARTED', 'PENDING'])
            # send_event('resume_parser','message',json.dumps({'task_id':task.id}))


            # return response to current client
            return JsonResponse({
                'response':'jobs run in background',
                'task_id':task.id,
                'total_resumes':metric['total'],
                # 'status_code': response.status_code,
            })
        
        else:

            response = JsonResponse({
                'response':'no resumes to parse',
            })
            response.status_code = 400
            return response
            
        
            
        