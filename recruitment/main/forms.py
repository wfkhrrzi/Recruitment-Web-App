from django.forms import ModelForm 
from .models import Screening, ScreeningSubmission, Users, Candidate
from django.http import HttpRequest

class ScreeningForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)

        for field in self.fields:
            if not field in self.Meta.required:
                self.fields[field].required = False

    class Meta:
        model = Screening
        # fields = ['candidate','selection_status']
        fields = '__all__'
        required = ('candidate','selection_status')

class ScreeningSubmissionForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        
        self.request:HttpRequest = kwargs.pop('request',None)

        super().__init__(*args,**kwargs)

        if self.request:
            if self.request.path.strip('/').split('/')[-1] == 'delete': # dependent on endpoint name
                self.fields['submission'].required = False
    
    class Meta:
        model = ScreeningSubmission
        fields = ['submission']
    

class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = '__all__'

class CandidatesForm(ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

