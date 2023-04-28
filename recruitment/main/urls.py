from django.urls import path

from . import view
from . import auth
from main.views.candidate import CandidateIndex,CandidateEdit
from main.views.pre_screening import PrescreeningCreate, PrescreeningSubmissionCreate, PrescreeningSubmissionDelete, PrescreeningInstructionSent, PrescreeningIndex
from main.views.init_screening import InitialScreeningIndex, InitialScreeningCreate, InitialScreeningEdit, InitialScreeningUpdate,InitialScreeningEvaluationCreate, InitialScreeningEvaluationDelete

app_name = 'main'

urlpatterns = [
    path('login', auth.login_view, name='login'),
    path('', view.index, name='index'),

    path('candidate', CandidateIndex.as_view(), name='candidate.index'),
    # path('candidate/edit/<int:screening_id>', CandidateEdit.as_view(), name='candidate.edit'),
    
    path('initscreening/<int:initial_screening_id>', InitialScreeningIndex.as_view(), name='initscreening.index'),
    path('initscreening/create', InitialScreeningCreate.as_view(), name='initscreening.create'),
    path("initscreening/update", InitialScreeningUpdate.as_view(), name='initscreening.update'),
    path("initscreening/evaluation/create", InitialScreeningEvaluationCreate.as_view(), name='initscreening.evaluation.create'),
    path("initscreening/evaluation/delete", InitialScreeningEvaluationDelete.as_view(), name='initscreening.evaluation.delete'),

    path('prescreening/<int:prescreening_id>', PrescreeningIndex.as_view(), name='prescreening.index'),
    path('prescreening/create', PrescreeningCreate.as_view(), name='prescreening.create'),
    path('prescreening/send_instruction', PrescreeningInstructionSent.as_view(), name='prescreening.send_instruction'),
    path("prescreening/submission/create", PrescreeningSubmissionCreate.as_view(), name='prescreening.submission.create'),
    path("prescreening/submission/delete", PrescreeningSubmissionDelete.as_view(), name='prescreening.submission.update'),

]