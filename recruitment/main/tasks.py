from celery import shared_task
from main.models import CandidateResume, Candidate, Status, Users, InitialScreening
from django.core.serializers import deserialize
import requests
import os
from typing import List
import time
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

@shared_task(bind=True)
def parse_resumes(self,job_title,job_description,resumes_json,user_id):

    # print({'job-title':job_title,'job-description':job_description,})

    user:Users = Users.objects.get(id=user_id)

    result_state = {
        'resumes_info':[],
        'user':{
            'id':user.pk,
            'alias':user.alias,
        },
    }

    self.update_state(state='STARTED',meta=result_state)

    # deserialize candidateresumes back to queryset
    deserialized_objects = list(deserialize('json', resumes_json))
    resumes_obj:List[CandidateResume] = [deserialized_object.object for deserialized_object in deserialized_objects]

    for resume in resumes_obj:
        resume.is_parsing=True
    CandidateResume.objects.bulk_update(resumes_obj,['is_parsing',])

    data = {
        'file_meta':[],
        'file_list':[],
    }

    # fetch filename and file from db
    for resume in resumes_obj:
        file_meta = dict(
            instance = resume,
            created_at = resume.created_at,
            name = resume.filename,
            source = resume.source,
            referral_name = resume.referral_name,
        )
        file_meta['instance'] = resume
        data['file_meta'].append(file_meta)
        resume_bytes = BytesIO(resume.submission)
        data['file_list'].append( ('file',InMemoryUploadedFile(
            resume_bytes, None, resume.filename, 'application/pdf', resume_bytes.tell(), None
        )) )
        
        result_state['resumes_info'].append({
            'name':resume.filename
        })

    self.update_state(state='STARTED',meta=result_state)

    # execute parsing process
    try:
        response = requests.post(
            'http://ptsg-5dspwb04-dstats2.azurewebsites.net/upload',
            data={
                'job_title':job_title,
                'job-description':job_description,
            },
            files=data['file_list'],
            # files=[('file',resume.submission.open(mode='rb')) for resume in resumes_obj],
        )
        # store parsing output into db
        parsed_resumes = dict(response.json())['parsed resumes']
    except: 
        print("*******************REVERT BACKK******************************")
        for resume in resumes_obj:
            resume.is_parsed = False
            resume.is_parsing = False
        CandidateResume.objects.bulk_update(resumes_obj,['is_parsed','is_parsing',])

        return "Error on the parser. Reverting resume parse status"
    
    new_candidates_list = []
    new_initialscreening_list = []
    
    try:
        for parsed_file in parsed_resumes:
            for file_meta in data['file_meta']:
                print(parsed_file['pdf_filename'] + ' | ' + os.path.splitext(os.path.basename(file_meta['name']))[0])
                if parsed_file['pdf_filename'] == os.path.splitext(os.path.basename(file_meta['name']))[0]:
                    new_candidate = Candidate(
                        name=parsed_file['Name'],
                        date=file_meta['created_at'],
                        referral_name=file_meta['referral_name'],
                        phone_number=parsed_file['StandardizedPhoneNumber'],
                        email=parsed_file['Email Address'],
                        highest_education=parsed_file['Education'],
                        years_exp=parsed_file['Total Years of Work Experience'],
                        CGPA=parsed_file['CGPA_value_nominator'],
                        # CGPA=float( parsed_file['CGPA'].split('/')[0].rstrip() ),
                        recent_role=parsed_file['Last Role'],
                        # recent_emp=None,
                        # recent_role=parsed_file['Last Role'],
                        main_skills=parsed_file['CandidateSkills'],
                        ds_skills=parsed_file['Relevant_data scientistskills'],
                        ds_background=parsed_file['Relevant_data scientistexperience'],
                        source=file_meta['source'],
                        created_by=Users.objects.get(id=user_id),
                        gpt_score=float(parsed_file['OverallCandidateScoreGPT'].split('/')[0]),
                        gpt_status= (
                            Status.objects.get(codename="gpt_status:not recommended") 
                            if parsed_file['Recommendation as data scientist (Yes/No)'].lower() == 'no'
                            else Status.objects.get(codename="gpt_status:recommended") 
                        ),
                        overall_status=Status.objects.get(codename='initscreening:pending'),
                        candidate_resume=file_meta['instance']
                        
                    )

                    new_candidate.save()
                    new_candidates_list.append(new_candidate)

                    initialscreening = InitialScreening(
                        candidate=new_candidate,
                        status=Status.objects.get(codename='initscreening:pending'),    
                    )
                    initialscreening.save()
                    # new_initialscreening_list.append(initialscreening)

                    data['file_meta'].remove(file_meta)

                    break

    except:
        
        print("*******************REVERT BACKK******************************")
        for resume in resumes_obj:
            resume.is_parsed = False
            resume.is_parsing = False
        CandidateResume.objects.bulk_update(resumes_obj,['is_parsed','is_parsing',])

        return "Error in DB. Reverting resume parse status"

    print(new_candidates_list)

    # Candidate.objects.bulk_create(new_candidates_list)
    # InitialScreening.objects.bulk_create(new_initialscreening_list)

    # Update is_parsed to parsed resumes
    for resume in resumes_obj:
        resume.is_parsed = True
        resume.is_parsing = False
    
    CandidateResume.objects.bulk_update(resumes_obj,['is_parsed','is_parsing',])

    return "Done"


@shared_task(bind=True)
def ping(self):
    self.update_state(state='STARTED',meta={'data':'custom data'})
    time.sleep(10)
    return "pong"
