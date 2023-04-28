from django.forms import ModelForm 
from .models import InitialScreening, Prescreening, PrescreeningSubmission, Users, Candidate
from django.http import HttpRequest

class InitialScreeningCreateForm(ModelForm):

    class Meta:
        model = InitialScreening
        fields = ['candidate']

class InitialScreeningUpdateForm(ModelForm):

    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(*args,**kwargs)

    #     for field in self.fields:
    #         if not field in self.Meta.required:
    #             self.fields[field].required = False

    class Meta:
        model = InitialScreening
        fields = ['candidate']

class PrescreeningForm(ModelForm):

    class Meta:
        model = Prescreening
        fields = []

class PrescreeningSubmissionForm(ModelForm):
    
    class Meta:
        model = PrescreeningSubmission
        fields = ['submission','prescreening']


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = '__all__'

class CandidatesForm(ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

