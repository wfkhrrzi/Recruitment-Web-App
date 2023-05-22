from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser

# Create your models here.

class UserPrivilege(models.Model):
    privilege = models.CharField(max_length=100)


class UserCategory(models.Model):
    category = models.CharField(max_length=100)


class UsersManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Users(PermissionsMixin,AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=10,null=True)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=200)
    user_privilege = models.ForeignKey(UserPrivilege,on_delete=models.SET_NULL,null=True)
    user_category = models.ForeignKey(UserCategory,on_delete=models.SET_NULL,null=True)

    #debugging admin site
    is_staff = models.BooleanField(default=False,)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','password']

    objects = UsersManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    class Meta:
        verbose_name='user'
        verbose_name_plural='users'


class Status(models.Model):
    codename = models.CharField(max_length=255,unique=True,null=True)
    status = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.status

class Source(models.Model):
    source = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.source

class EmpCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category


class LastModifiedMixin(models.Model):

    last_modified_at = models.DateTimeField(auto_now=True,null=True)
    last_modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True, related_name="%(app_label)s_%(class)s_last_modified_by")

    class Meta:
        abstract = True

class CreatedMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name="%(app_label)s_%(class)s_user_created_by")
    
    class Meta:
        abstract = True


class Candidate(CreatedMixin,LastModifiedMixin,models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    referral_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    highest_education = models.CharField(max_length=100) # need revision on this
    years_exp = models.IntegerField()
    CGPA = models.FloatField()
    recent_role = models.CharField(max_length=100)
    recent_emp = models.CharField(max_length=100)
    main_skills = models.CharField(max_length=100)
    ds_skills = models.CharField(max_length=100)
    ds_background = models.CharField(max_length=100)
    hr_remarks = models.TextField(null=True)
    gpt_status = models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,related_name="candidates_gpt_status")
    cv_link = models.CharField(max_length=255)
    source = models.ForeignKey(Source,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(EmpCategory,on_delete=models.SET_NULL,null=True)
    overall_status = models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,related_name="candidates_overall_status")

    def __str__(self) -> str:
        return self.name


class InitialScreening(LastModifiedMixin,models.Model):
    candidate = models.OneToOneField(Candidate,on_delete=models.CASCADE)
    is_hm_proceed = models.BooleanField(null=True)
    hm_date_selected = models.DateField(null=True)
    hm_status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True,related_name="initialscreening_hm_status")
    date_selected = models.DateField(null=True)
    is_proceed = models.BooleanField(null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True,related_name="initialscreening_final_status")
    remarks = models.TextField(null=True)
    # revision for assessment results 


class InitialScreeningEvaluation(CreatedMixin,LastModifiedMixin,models.Model):
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,related_name='initialscreeningevaluation_user')
    initial_screening = models.ForeignKey(InitialScreening,on_delete=models.CASCADE)
    is_proceed = models.BooleanField(null=True)


class Submission(CreatedMixin,models.Model):

    def upload_directory(self,filename):
        model_name = self._meta.model_name

        if model_name == PrescreeningSubmission._meta.model_name:
            ps_obj:PrescreeningSubmission = self
            return f"Prescreening/{ps_obj.prescreening.candidate.name}/{filename}"
        elif model_name == CBISubmission._meta.model_name:
            cs_obj:CBISubmission = self
            return f"CBI/{cs_obj.cbi.candidate.name}/{filename}"            
        elif model_name == CandidateResume._meta.model_name:
            return f"Resume/{filename}"            

    submission = models.FileField(upload_to=upload_directory)
    is_active = models.BooleanField(default=True,null=False)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='%(app_label)s_%(class)s_deleted_by')

    def delete(self,commit:bool=True):
        '''Set self.is_active = False'''
        self.is_active = False
        
        if commit:
            self.save()
            return None
        else:
            return self

    class Meta:
        abstract = True


class Prescreening(CreatedMixin,LastModifiedMixin,models.Model):
    candidate = models.OneToOneField(Candidate,on_delete=models.CASCADE,null=False)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False,related_name='prescreening_status')
    assessment_status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True,related_name='prescreening_assessment_status')
    is_proceed = models.BooleanField(null=True)
    is_sent_instruction = models.BooleanField(default=False)
    instruction_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def reset_instance(self):
        self.status = Status.objects.get(codename='prescreening:send instruction')
        self.assessment_status = Status.objects.get(codename='prescreening:send instruction')
        self.is_proceed = None
        self.is_sent_instruction = False
        self.instruction_date = None
        self.is_active = False

        self.save()

    def activate_instance(self):
        self.is_active = True

        self.save()

class PrescreeningSubmission(Submission):

    prescreening = models.ForeignKey(Prescreening,on_delete=models.CASCADE,null=False,blank=False)


class CBI(CreatedMixin,LastModifiedMixin,models.Model):
    remarks = models.TextField(null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    candidate = models.OneToOneField(Candidate,on_delete=models.CASCADE,null=False)
    is_proceed = models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)

    def reset_instance(self):
        self.status = Status.objects.get(codename='cbi:pending schedule')
        self.is_proceed = None
        self.remarks = None
        self.is_active = False

        self.save()

    def activate_instance(self):
        self.is_active = True

        self.save()


class CBISchedule(CreatedMixin,LastModifiedMixin,models.Model):
    cbi = models.ForeignKey(CBI,on_delete=models.CASCADE,null=False)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    datetime = models.DateTimeField()
    remarks = models.TextField(null=True,blank=True)
    assessor1 = models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='user1_CBISchedule',null=True)
    assessor1_status = models.ForeignKey(Status,on_delete=models.SET_NULL,related_name='user1_status',null=True)
    assessor2 = models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='user2_CBISchedule',null=True,blank=True)
    assessor2_status = models.ForeignKey(Status,on_delete=models.SET_NULL,related_name='user2_status',null=True,blank=True)
    assessor3 = models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='user3_CBISchedule',null=True,blank=True)
    assessor3_status = models.ForeignKey(Status,on_delete=models.SET_NULL,related_name='user3_status',null=True,blank=True)
    is_proceed = models.BooleanField(null=True)
    is_RSVP = models.BooleanField(default=False)


class CBISubmission(Submission):
    
    cbi = models.ForeignKey(CBI,on_delete=models.CASCADE,null=False,blank=False)
    

class Hiring(models.Model):
    salary_proposal = models.DateField(null=True)
    offer_letter_rollout = models.DateField(null=True)
    offer_letter_accept = models.DateField(null=True)
    remark = models.TextField(null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    candidate = models.OneToOneField(Candidate,on_delete=models.CASCADE,null=False)

class CandidateResume(Submission):
    
    # candidate = models.ForeignKey(Candidate, null=True, on_delete=models.SET_NULL)
    candidate_name = models.CharField(max_length=200,null=True)
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)
    referral_name = models.CharField(max_length=200,null=True,)
    