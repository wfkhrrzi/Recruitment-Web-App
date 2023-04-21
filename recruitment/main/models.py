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


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    referral_name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(max_length=100)
    last_modified_by = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
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
    cv_link = models.CharField(max_length=255)
    source = models.ForeignKey(Source,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(EmpCategory,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.name

class InitialScreening(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    selection_status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    remarks = models.TextField(null=True)
    selection_date = models.DateField(null=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True)
    # revision for assessment results 

class InitialScreeningEvaluation(models.Model):
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,related_name='initscreening_user')
    initial_screening = models.ForeignKey(InitialScreening,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='initscreening_user_created_by')

class Prescreening(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
    initial_screening = models.ForeignKey(InitialScreening,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='prescreening_user_created_by')
    last_modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='prescreening_user_last_modified_by')



class Submission(models.Model):

    def upload_directory(instance):
        raise NotImplementedError

    submission = models.FileField(upload_to=upload_directory)
    is_active = models.BooleanField(default=True,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self):
        '''Set self.is_active = False'''
        self.is_active = False
        self.save()

    class Meta:
        abstract = True

class PrescreeningSubmission(Submission):

    def upload_directory(instance,filename):
        return f"Prescreening/{instance.initial_screening.candidate.name}/{filename}"

    prescreening = models.ForeignKey(InitialScreening,on_delete=models.CASCADE,null=False,blank=False)

class CBI(models.Model):
    date = models.DateField(null=True)
    remarks = models.TextField(null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='cbi_user_created_by')
    last_modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='cbi_user_last_modified_by')

class CBISchedule(models.Model):
    cbi = models.ForeignKey(CBI,on_delete=models.CASCADE,null=False)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    datetime = models.DateTimeField()
    remarks = models.TextField(null=True)
    assessor1 = models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='user1_CBISchedule',null=True)
    assessor1_status = models.ForeignKey(Status,on_delete=models.SET_NULL,related_name='user1_status',null=True)
    assessor2 = models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='user2_CBISchedule',null=True)
    assessor2_status = models.ForeignKey(Status,on_delete=models.SET_NULL,related_name='user2_status',null=True)
    assessor3 = models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='user3_CBISchedule',null=True)
    assessor3_status = models.ForeignKey(Status,on_delete=models.SET_NULL,related_name='user3_status',null=True)

class CBISubmission(Submission):
    
    def upload_directory(instance,filename):
        return f"CBI/{instance.cbi.candidate.name}/{filename}"
    
    cbi = models.ForeignKey(CBI,on_delete=models.CASCADE,null=False,blank=False)

class Hiring(models.Model):
    salary_proposal = models.DateField(null=True)
    offer_letter_rollout = models.DateField(null=True)
    offer_letter_accept = models.DateField(null=True)
    remark = models.TextField(null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=False)
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,null=False)
