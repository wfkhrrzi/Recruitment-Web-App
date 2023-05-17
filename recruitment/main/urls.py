from django.urls import path

from . import view
from . import auth
from main.views.candidate import CandidateIndex,CandidateEdit
from main.views.prescreening import PrescreeningCreate, PrescreeningSubmissionCreate, PrescreeningSubmissionDelete, PrescreeningInstructionSent, PrescreeningIndex, PrescreeningUpdate
from main.views.initscreening import InitialScreeningIndex, InitialScreeningCreate, InitialScreeningEdit, InitialScreeningUpdate,InitialScreeningEvaluationCreate, InitialScreeningEvaluationDelete, InitialScreeningHiringUpdate
from main.views.cbi import CBICreate, CBIIndex, CBIScheduleCreate, CBIScheduleUpdate, CBISubmissionCreate, CBISubmissionDelete
from main.view import BrowseIndex, BrowseView

app_name = 'main'

urlpatterns = [
    path('api/login', auth.login_view, name='login'),
    path('login', auth.CustomLoginView.as_view(), name='login'),
    path('', view.index, name='index'),
    path('browse', BrowseIndex.as_view(), name='browse.index'),
    path('browse/<int:candidate_id>', BrowseView.as_view(), name='browse.view'),

    path('candidate', CandidateIndex.as_view(), name='candidate.index'),
    # path('candidate/edit/<int:screening_id>', CandidateEdit.as_view(), name='candidate.edit'),
    
    path('initialscreening/', InitialScreeningIndex.as_view(), name='initscreening.index.default'),
    path('initialscreening/<int:initial_screening_id>', InitialScreeningIndex.as_view(), name='initscreening.index'),
    path('initialscreening/create', InitialScreeningCreate.as_view(), name='initscreening.create'),
    path("initialscreening/hiring/update", InitialScreeningHiringUpdate.as_view(), name='initscreening.hiring.update'),
    path("initialscreening/update", InitialScreeningUpdate.as_view(), name='initscreening.update'),
    path("initialscreening/evaluation/create", InitialScreeningEvaluationCreate.as_view(), name='initscreening.evaluation.create'),
    path("initialscreening/evaluation/delete", InitialScreeningEvaluationDelete.as_view(), name='initscreening.evaluation.delete'),

    path('prescreening/', PrescreeningIndex.as_view(), name='prescreening.index.default'),
    path('prescreening/<int:prescreening_id>', PrescreeningIndex.as_view(), name='prescreening.index'),
    path('prescreening/create', PrescreeningCreate.as_view(), name='prescreening.create'),
    path('prescreening/update', PrescreeningUpdate.as_view(), name='prescreening.update'),
    path('prescreening/send_instruction', PrescreeningInstructionSent.as_view(), name='prescreening.send_instruction'),
    path("prescreening/submission/create", PrescreeningSubmissionCreate.as_view(), name='prescreening.submission.create'),
    path("prescreening/submission/delete", PrescreeningSubmissionDelete.as_view(), name='prescreening.submission.update'),

    path('cbi/', CBIIndex.as_view(), name='cbi.index.default'),
    path('cbi/<int:cbi_id>', CBIIndex.as_view(), name='cbi.index'),
    path('cbi/create', CBICreate.as_view(), name='cbi.create'),
    path('cbi/schedule/create', CBIScheduleCreate.as_view(), name='cbi.schedule.create'),
    path('cbi/schedule/update', CBIScheduleUpdate.as_view(), name='cbi.schedule.update'),
    path("cbi/submission/create", CBISubmissionCreate.as_view(), name='cbi.submission.create'),
    path("cbi/submission/delete", CBISubmissionDelete.as_view(), name='cbi.submission.update'),


]