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
    'prescreening:assessment submitted':'ready for validation', # not needed
    # 'prescreening:hackerrank passed':'Passed',
    # 'prescreening:hackerrank failed':'Failed',
    'prescreening:proceed':'proceed',
    'prescreening:not proceed':'not proceed',
    # proceed for hr prescreen
    # proceed to CBI

    'cbi:proceed':'recommended',
    'cbi:not proceed':'not recommended',
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

lst_nationality = ['Local','Expat']
lst_emp_category = ['Fresh DS', 'Head', 'Experienced DS', 'Intern', 'GEES', 'Internal Mobility', 'RTT']
lst_source = [
    'Referral',
    'CADS',
    'Unknown',
    'Mobility',
    'Career Day',
    'University',
    'GEES',
    'Headhunter',
    'LinkedIn',
    'MyCareerX',
    'PESP1',
    'PESP2 Master Programme'
]
lst_user_category = ['DS Lead', 'HR', 'Admin']
lst_ds_leads = ['Dr Samba','Dr Assad','Dr Vikram','Dr Tosin','Dr Liang','Dr Khor','Dr Bassam','Dr Premeela','Aleks','Marc','Krishna','Neeraj','Prem Kumar']

class StatusFactory(DjangoModelFactory):
    
    class Meta:
        model = Status
        
    
    codename = Iterator(lst_codename)
    status = Iterator(lst_status)


class NationalityFactory(DjangoModelFactory):
    
    class Meta:
        model = Nationality
        
    
    nationality = Iterator(lst_nationality)


class EmpCategoryFactory(DjangoModelFactory):
    class Meta:
        model = EmpCategory

    category = Iterator(lst_emp_category)


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source

    source = Iterator(lst_source)

class UserCategoryFactory(DjangoModelFactory):
    class Meta:
        model = UserCategory

    category = Iterator(lst_user_category)

class BaseUsersFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    alias = LazyAttribute(lambda m: m.first_name)
    email = LazyAttribute(lambda m: f"{m.first_name.lower()}_{m.last_name.lower()}@test.com")
    user_name = LazyAttribute(lambda m: m.email.split('@')[0])
    password = make_password('test')    


class UsersFactory(BaseUsersFactory):
    class Meta:
        model = Users
    
    is_superuser = False
    is_staff = True
    user_category = LazyAttribute(lambda o:random.choice(UserCategory.objects.all()))


class AdminFactory(BaseUsersFactory):
    class Meta:
        model = Users
    
    is_superuser = True
    is_staff = True
    user_category = LazyAttribute(lambda o:UserCategory.objects.get(category__iexact='admin'))


class DSLeadFactory(BaseUsersFactory):
    class Meta:
        model = Users
    
    first_name=Iterator(lst_ds_leads)
    last_name=''
    alias=Iterator(lst_ds_leads)
    email = LazyAttribute(lambda m: f"{m.first_name.lower().replace(' ','')}@test.com")
    is_superuser = False
    is_staff = True
    user_category = LazyAttribute(lambda o:UserCategory.objects.get(category__iexact='ds lead'))


class CandidateFactory(DjangoModelFactory):
    class Meta:
        model = Candidate
    
    name = Faker('name')
    date = Faker('date_between',start_date="-30d",end_date="today")
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
       

class ParseConfigurationFactory(DjangoModelFactory):

    class Meta:
        model = ParserConfiguration

    job_title = 'data scientist'
    job_description = """This is for example is our JD for experienced data scientist:\n
Responsible for design, planning, and coordinating the implementation of Data Science work activities in the Group Digital with established structured processes and procedures to support PETRONAS's digital agenda.\n
1) Technical & Professional Excellence

Responsible for ensuring data required for analytic models is of required quality and models are constructed to standards and deployed effectively.
Implement data science industry best practices, relevant cutting-edge technology, and innovation in projects to ensure the right solutions fulfill the business requirements.

2) Technical/Skill Leadership & Solutioning

Responsible for developing appropriate technical solutions to address business pain points with insights and recommendations.
Implement an established analytics strategy by adopting the right technologies and technical requirements when executing projects to ensure business value generation.
Execute operational excellence through continuous technical and process improvement initiatives within projects to improve operations efficiency and effectiveness within own activity & projects.

3) Technical Expertise

Track and follow up with relevant parties to ensure Technical Excellence Programmes are successfully deployed and integrated into work processes, documents, policies, and guidelines.
Participate in a community of practices and network with internal and external technical experts by identifying solutions to common problems and capturing and sharing existing data science knowledge for continuous excellence.


Be part of our DS team in at least one of the following areas:

Machine Learning

Roles: Design analytics solutions for business problems; develop, evaluate, optimize, deploy and maintain models.

Tech stack: ML Algorithms, Python, SQL, Spark, Git, Cloud Services, Deep Learning frameworks, MLOps, etc


Natural Language Processing

Roles: Design text analytics solutions for business problems; develop, evaluate, optimize, deploy and maintain text processing and analytics solutions.

Tech stack: Python, SQL, Git, NLTK, Deep Learning frameworks, MLOps, Text analytics, NLP, NLU, NLG, Language Models, etc


Computer Vision

Roles: Design Image and video analytics solutions for business problems; develop, evaluate, optimize, deploy and maintain solutions

Tech stack: Tensorflow, OpenCV, Fastai, Pytorch, MLFlow, Spark, MLlib Python, SQL, Git, Deep Learning frameworks, MLOps, etc


Optimization / Simulation

Roles: Design optimization/simulation analytics solutions for business problems; develop, evaluate, optimize, deploy and maintain solutions

Tech stack: mathematical/process models, Simulation modeling, AnyLogic, Simio, mixed-integer programming (linear and nonlinear), Python, Pyomo, Gurobi solver, MLOps, etc.

What are the requirements?

Bachelor's or Master's degree in Data Science, Mathematics, Engineering, Computer Science, or in any other discipline
At least 2 years of relevant experience covering advanced statistical analysis and machine learning.
Good in statistical and scripting programming languages (such as R, Python, and MATLAB)"""