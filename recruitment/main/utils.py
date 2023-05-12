import inspect
from main.models import Candidate
from django.db import models
from django.db.models import F

def return_json(request):
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return True
    else:
        return False
    
def extract_candidate_info(model_instance)->dict:

    if not isinstance(model_instance,models.Model):
        raise ValueError('parameter is not a model.Models instance')

    if not hasattr(model_instance, 'candidate'):
        raise ValueError('model instance does not have candidate')

    dict_candidate = Candidate.objects.filter(id=model_instance.candidate.id).annotate(
        gpt_status_ = F('gpt_status__status'),
        source_ = F('source__source'),
        category_ = F('category__category'),
        overall_status_ = F('overall_status__status'),
    ).values(
        "last_modified_at",
        "last_modified_by",
        "created_at",
        "created_by",
        "name",
        "date",
        "referral_name",
        "phone_number",
        "email",
        "highest_education",
        "years_exp",
        "CGPA",
        "recent_role",
        "recent_emp",
        "main_skills",
        "ds_skills",
        "ds_background",
        "hr_remarks",
        "cv_link",
        "gpt_status_",
        "source_",
        "category_",
        "overall_status_",
    )

    return list(dict_candidate)[0]