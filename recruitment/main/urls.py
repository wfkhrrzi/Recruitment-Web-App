from django.urls import path

from . import view
from . import auth
from main.views.candidate import CandidateIndex,CandidateEdit
from main.views.screening import ScreeningCreate,ScreeningUpdate,ScreeningSubmissionCreate,ScreeningSubmissionDelete

app_name = 'main'

urlpatterns = [
    path('login', auth.login_view, name='login'),
    path('', view.index, name='index'),

    path('candidate', CandidateIndex.as_view(), name='candidate.index'),
    path('candidate/edit/<int:screening_id>', CandidateEdit.as_view(), name='candidate.edit'),
    
    path('screening/create', ScreeningCreate.as_view(), name='screening.create'),
    path("screening/update", ScreeningUpdate.as_view(), name='screening.update'),
    path("screening/submission/create", ScreeningSubmissionCreate.as_view(), name='screening.submission.create'),
    path("screening/submission/delete", ScreeningSubmissionDelete.as_view(), name='screening.submission.update'),

]