from factory.django import DjangoModelFactory
from main.models import *
from factory import Faker, Iterator, SubFactory, LazyAttribute, Sequence
from typing import List
from django.contrib.auth.hashers import make_password
import random

dict_status = {
    'initscreening:pending':'Yet to select',
    'initscreening:selected':'selected',
    'initscreening:not selected':'not selected',
    'initscreening:proceed':'proceed',
    'initscreening:not proceed':'not proceed',

    'prescreening:pending':'pending',
    'prescreening:send instruction':'pending instruction',
    'prescreening:pending submission':'pending response',
    'prescreening:assessment submitted':'ready for validation',
    'prescreening:proceed':'proceed',
    'prescreening:not proceed':'not proceed',

    'cbi:proceed':'proceed',
    'cbi:not proceed':'not proceed',
    'cbi:pending interview':'pending interview',
    'cbi:pending result':'pending result',
    'cbi:pending schedule':'pending schedule', # add cbi:pending schedule

    'cbi_schedule:unscheduled':'unscheduled',
    'cbi_schedule:pending send RSVP':'pending RSVP invitation',
    'cbi_schedule:pending RSVP response':'pending RSVP response',
    'cbi_schedule:RSVP proceed':'available',
    'cbi_schedule:RSVP cancel':'unavailable',
    'cbi_schedule:rescheduled':'cancelled',
    'cbi_schedule:conducted':'conducted',

    'gpt_status:recommended':'recommended',
    'gpt_status:not recommended':'not recommended',
    
    # 'proceed':'proceed',
    # 'do not proceed':'do not proceed',
    # 'accepted':'accepted',
    # 'rejected':'rejected',
    # 'pending':'pending',
    # 'recommended':'recommended',
    # 'not recommended':'not recommended',

    'initscreening:ongoing':'ongoing initial screening',
    'prescreening:ongoing':'ongoing prescreening',
    'cbi:ongoing':'ongoing cbi',
}

lst_codename = list()
lst_status = list()

for key, value in dict_status.items():
    lst_codename.append(key)
    lst_status.append(value)


class StatusFactory(DjangoModelFactory):
    
    class Meta:
        model = Status
        
    
    codename = Iterator(lst_codename)
    status = Iterator(lst_status)


class EmpCategoryFactory(DjangoModelFactory):
    class Meta:
        model = EmpCategory

    category = Iterator(['Fresh DS', 'Head', 'Experienced DS'])


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source

    source = Iterator(['LinkedIn', 'HeadHunter', 'JobStreet'])


class UsersFactory(DjangoModelFactory):
    class Meta:
        model = Users
    
    email = Sequence(lambda i: f"user{i}@test.com")
    password = make_password('test')
    user_name = LazyAttribute(lambda m: m.email.split('@')[0])
    is_superuser = False
    is_staff = True

class AdminFactory(DjangoModelFactory):
    class Meta:
        model = Users
    
    email = Sequence(lambda i: f"admin{i}@test.com")
    password = make_password('test')
    user_name = LazyAttribute(lambda m: m.email.split('@')[0])
    is_superuser = True
    is_staff = True


class CandidateFactory(DjangoModelFactory):
    class Meta:
        model = Candidate
    
    name = Faker('name')
    date = Faker('date_between',start_date="-15d",end_date="today")
    referral_name = Faker('name')
    phone_number = Faker('phone_number')
    email = LazyAttribute(lambda m: f"{''.join(m.name.lower().split())}@example.com")
    highest_education = Iterator(['bachelor', 'diploma', 'master', 'phd'])
    years_exp = Faker('random_digit_not_null')
    cv_link = LazyAttribute(lambda m: f"https://petronas.onedrive.com/{m.name}-resume.pdf")
    CGPA = Faker('pyfloat',min_value=3,max_value=4,right_digits=2,positive=True)
    recent_role = Faker('job')
    recent_emp = Faker('company')
    main_skills = Faker('text')
    ds_skills = Faker('text')
    ds_background = Faker('text')
    hr_remarks = Faker('text')
    gpt_status = LazyAttribute(lambda o:random.choice(Status.objects.filter(codename__in=['gpt_status:recommended','gpt_status:not recommended',])))
    source = LazyAttribute(lambda o:random.choice(Source.objects.all()))
    category = LazyAttribute(lambda o:random.choice(EmpCategory.objects.all()))
    overall_status = LazyAttribute(lambda o:random.choice(Status.objects.filter(codename__in=[
        'initscreening:ongoing',
    ])))
    


class InitialScreeningFactory(DjangoModelFactory):
    
    class Meta:
        model = InitialScreening

    candidate = Iterator(Candidate.objects.all())
    status= LazyAttribute(lambda o:Status.objects.get(codename='initscreening:pending'))
       
