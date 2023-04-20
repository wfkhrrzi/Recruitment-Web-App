from factory.django import DjangoModelFactory
from main.models import *
from factory import Faker, Iterator, SubFactory, LazyAttribute, Sequence
from typing import List
from django.contrib.auth.hashers import make_password
import random


class StatusFactory(DjangoModelFactory):
    class Meta:
        model = Status

    status = Iterator(['pending', 'KIV', 'Not screened'])


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
    email = LazyAttribute(lambda m: f"{m.name}@example.com")
    highest_education = Iterator(['bachelor', 'diploma', 'master', 'phd'])
    years_exp = Faker('random_digit_not_null')
    cv_link = LazyAttribute(lambda m: f"https://petronas.onedrive.com/{m.name}-resume.pdf")
    created_at = Faker('iso8601')
    modified_at = Faker('iso8601')
    CGPA = round(random.uniform(3,4),2)
    recent_role = Faker('job')
    recent_emp = Faker('company')
    main_skills = Faker('text')
    ds_skills = Faker('text')
    ds_background = Faker('text')
    hr_remarks = Faker('text')
    source = LazyAttribute(lambda o:random.choice(Source.objects.all()))
    category = LazyAttribute(lambda o:random.choice(EmpCategory.objects.all()))


       
