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
    'prescreening:send instruction':'pending instruction',
    'prescreening:pending submission':'pending response',
    'prescreening:assessment submitted':'ready for validation',
    'cbi:send invitation':'pending RSVP invitation',
    'cbi:rescheduled':'cancelled',
    'cbi:conducted':'conducted',
    'proceed':'proceed',
    'do not proceed':'do not proceed',
    'accepted':'accepted',
    'rejected':'rejected',
    'pending':'pending',
    'recommended':'recommended',
    'not recommended':'not recommended',        
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
    date = Faker('date')
    referral_name = Faker('name')
    phone_number = Faker('phone_number')
    email = LazyAttribute(lambda m: f"{''.join(m.name.lower().split())}@example.com")
    highest_education = Iterator(['bachelor', 'diploma', 'master', 'phd'])
    years_exp = Faker('random_digit_not_null')
    cv_link = LazyAttribute(lambda m: f"https://petronas.onedrive.com/{m.name}-resume.pdf")
    # created_at = Faker('iso8601')
    # modified_at = Faker('iso8601')
    CGPA = Faker('pyfloat',min_value=3,max_value=4,right_digits=2,positive=True)
    recent_role = Faker('job')
    recent_emp = Faker('company')
    main_skills = Faker('text')
    ds_skills = Faker('text')
    ds_background = Faker('text')
    hr_remarks = Faker('text')
    source = LazyAttribute(lambda o:random.choice(Source.objects.all()))
    category = LazyAttribute(lambda o:random.choice(EmpCategory.objects.all()))


       
