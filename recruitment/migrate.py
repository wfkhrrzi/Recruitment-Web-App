import pandas as pd
import django
import os
import pandas as pd
from io import BytesIO
from datetime import datetime
import random
from tqdm import tqdm
from typing import List

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")
django.setup()

# Import your Django models
from main.models import Candidate,Source,EmpCategory,Status,CandidateResume,Nationality,InitialScreening,InitialScreeningEvaluation,Users,Prescreening,CBI,CBISchedule

def migrate_data():

    print('Start migration...')

    directory = 'D://Study Stuffs//OneDrive - Universiti Teknologi MARA//Degree UiTM//DEGREE INTERNSHIP//PETRONAS DIGITAL//Copied Documents from Laptop//Migration Resumes'
    # df = pd.read_csv('C://PET DIG Projects//LOCAL Recruitment//Existing Candidates MIGRATION//new_recruitment_preprocessed.csv',)
    df = pd.read_csv('D:/Study Stuffs/OneDrive - Universiti Teknologi MARA/Degree UiTM/DEGREE INTERNSHIP/PETRONAS DIGITAL/Copied Documents from Laptop/existing_candidates_parsed_final.csv',)

    # Retrieve files in the directory
    files = os.listdir(directory)

    # Iterate over the candidates
    candidates_list = []
    initialscreening_list = []
    initialscreening_eval_list = []
    prescreening_list = []
    cbi_list = []
    cbi_schedule_list:List[CBISchedule] = []

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):

        try:
            source = Source.objects.get(source=row['Source'])
        except:
            source = None

        try:
            category = EmpCategory.objects.get(category=row['Category'])
        except:
            category = None

        if pd.isnull(row['Received Date']): 
            date = None
        else:
            date = datetime.strptime(row['Received Date'], '%Y-%m-%d').date()

        candidate = Candidate(
            name = row['Candidate Name'],
            nationality = Nationality.objects.get(nationality=row['Nationality']),
            source = source,
            category = category,
            date = date,
            referral_name = row['Referred By'],
            overall_remarks = None if row['Remark'] == 'null' or pd.isnull(row['Remark']) else row['Remark'],
            email = row['email'],
            highest_education = row['highest_education'],
            years_exp = row['years_exp'],
            CGPA = row['CGPA'],
            recent_role = row['recent_role'],
            recent_emp = row['recent_emp'],
            main_skills = row['main_skills'],
            ds_skills = row['ds_skills'],
            ds_background = row['ds_background'],
            phone_number = row['phone_number'],
            gpt_score = row['gpt_score'] if not pd.isnull(row['gpt_score']) else 20,
            gpt_status = Status.objects.get(codename='gpt_status:recommended') if row['gpt_status'] == 'Yes' else Status.objects.get(codename='gpt_status:not recommended') if row['gpt_status'] == 'No' else None

        )

        for file in files:
            if f"resume_{row['id']}.pdf" in file:
                resume = CandidateResume(submission=open(directory+'/'+file,'rb').read(), filename=file, is_parsed=True)
                resume.save()
                
                candidate.cv_link = file
                candidate.candidate_resume = resume

                break
        
        #initial screening

        is_proceed = bool(row['Selection']) if not pd.isnull(row['Selection']) else None
        is_hm_proceed = None if is_proceed == None else False if row[7:20].isna().all() and is_proceed else True
        
        is_status = Status.objects.get(codename='initscreening:proceed' if is_proceed == True else 'initscreening:not proceed' if is_proceed == False else 'initscreening:pending')
        is_hm_status = Status.objects.get(codename='initscreening:proceed' if is_hm_proceed else 'initscreening:not proceed') if is_hm_proceed != None else None

        initialscreening = InitialScreening(
            candidate=candidate,
            hm_status=is_hm_status,
            is_hm_proceed=is_hm_proceed,
            is_proceed=is_proceed,
            status=is_status,
            date_selected=datetime.strptime(row['Selection Date'], '%Y-%m-%d').date() if pd.isnull(row['Selection Date']) != True else None,
            remarks=row['Comment/Remarks'] if pd.isnull(row['Comment/Remarks']) != True else None,
        )

        candidate.overall_status = Status.objects.get(codename="initscreening:pending" if is_proceed else "initscreening:not proceed" )

        candidates_list.append(candidate)
        initialscreening_list.append(initialscreening)

        for lead,selection in row[7:20].to_dict().items():
            if not pd.isnull(selection):
                initialscreening_eval_list.append(
                    InitialScreeningEvaluation(
                        initial_screening=initialscreening,
                        is_proceed=bool(selection),
                        status=Status.objects.get(codename='initscreening:proceed' if bool(selection) else 'initscreening:not proceed'),
                        user=Users.objects.get(alias__iexact=lead),
                    )
                )

        # prescreening, cbi
        prescreening = Prescreening(candidate=candidate)
        prescreening.status = Status.objects.get(codename='prescreening:send instruction')
        prescreening.assessment_status = Status.objects.get(codename='prescreening:send instruction')

        cbi = CBI(candidate=candidate)
        cbi.status = Status.objects.get(codename='cbi:pending prescreen')

        cbi_schedule = None
        if not pd.isnull(row['CBI - Interview Date']):
            cbi_schedule = CBISchedule(
                cbi=cbi,
                datetime=datetime.strptime(row['CBI - Interview Date'].replace('\xa0', ' '), "%Y-%m-%d %H:%M:%S"),
                status=Status.objects.get(codename='cbi_schedule:conducted')
            )

            cbi_schedule_list.append(cbi_schedule)


        if pd.isnull(row['Selection']):
            
            candidate.overall_status = initialscreening.status

        elif row['Joining Status'] == 'Not Shortlisted':
            pass # already created initial screening above

        # filter by joining status == pending
        elif row['Joining Status'] == 'Pending':

            initialscreening.status = Status.objects.get(codename='initscreening:mobility')
            initialscreening.is_proceed = None

            candidate.overall_status = initialscreening.status
        
        # filter by remarks containing 'salary' 
        elif not pd.isnull(row['Remark']) and 'salary' in row['Remark'].lower():
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            if row['Joining Status'] == 'Recruited':
                cbi.is_proceed = True
                cbi.status = Status.objects.get(codename='cbi:proceed')
            else:
                cbi.is_proceed = False
                cbi.status = Status.objects.get(codename='cbi:not proceed')


            prescreening_list.append(prescreening)
            cbi_list.append(cbi)
            candidate.overall_status = Status.objects.get(codename=f"joining:{'withdraw' if row['Joining Status'].lower() != 'recruited' else row['Joining Status'].lower() }")

        # filter by remarks containing prescreen remarks
        elif not pd.isnull(row['Remark'])  \
        and ( 'screen' in row['Remark'].lower() \
        or 'interview' in row['Remark'].lower() \
        or 'pre-screen' in row['Remark'].lower() \
        or 'solution' in row['Remark'].lower() ):

            prescreening.is_proceed = False
            prescreening.status = Status.objects.get(codename='prescreening:not proceed')

            prescreening_list.append(prescreening)
            candidate.overall_status = Status.objects.get(codename=f"joining:withdraw")

        # filter by remarks containing cbi result
        elif not pd.isnull(row['Remark']) and 'cbi result' in row['Remark'].lower():
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            cbi.status = Status.objects.get(codename='cbi:pending result')

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)
            candidate.overall_status = cbi.status

        # filter by joining status == pending  cbi
        elif row['Joining Status'] == 'Pending CBI':
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            cbi.status = Status.objects.get(codename='cbi:pending schedule')

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)
            candidate.overall_status = cbi.status

        # filter by joining status == pending hkr (hackerrank) result
        elif row['Joining Status'] == 'Pending HKR Result':
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:pending submission')

            prescreening_list.append(prescreening)
            candidate.overall_status = prescreening.status

        # filter by joining status == pending prescreen
        elif row['Joining Status'] in ('Pending Pre screen',):
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')
            
            cbi.status = Status.objects.get(codename='cbi:pending prescreen')

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)
            candidate.overall_status = cbi.status

        elif row['Joining Status'] in ('Not Recommended','Withdraw','Hold'):
            if (cbi_schedule):
                prescreening.is_proceed = True
                prescreening.status = Status.objects.get(codename='prescreening:proceed')
                cbi.is_proceed = False
                cbi.status = Status.objects.get(codename=f"cbi:{'not proceed' if row['Joining Status'] == 'Not Recommended' else 'withdraw' if row['Joining Status'] == 'Withdraw' else 'hold'}")
                prescreening_list.append(prescreening)
                cbi_list.append(cbi)
                
                candidate.overall_status = cbi.status

            else:
                prescreening.is_proceed = False
                prescreening.status = Status.objects.get(codename=f"prescreening:{'not proceed' if row['Joining Status'] == 'Not Recommended' else 'withdraw' if row['Joining Status'] == 'Withdraw' else 'hold'}")
                prescreening_list.append(prescreening)
                
                candidate.overall_status = prescreening.status


        # filter by status Recruited, Declined, Pending SP
        elif row['Joining Status'] in ('Recruited','Declined ','Pending SP'):
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')
            cbi.is_proceed = True
            cbi.status = Status.objects.get(codename='cbi:proceed')

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)
            candidate.overall_status = Status.objects.get(codename=f"joining:{'withdraw' if row['Joining Status'].lower() == 'declined ' else row['Joining Status'].lower() }")

        # discard schedule that does not have cbi
        for i,cbi_schedule in enumerate(cbi_schedule_list):
            if cbi_schedule.cbi not in cbi_list:
                cbi_schedule_list.pop(i)

    # Bulk create instances
    Candidate.objects.bulk_create(candidates_list)
    InitialScreening.objects.bulk_create(initialscreening_list)
    InitialScreeningEvaluation.objects.bulk_create(initialscreening_eval_list)
    Prescreening.objects.bulk_create(prescreening_list)
    CBI.objects.bulk_create(cbi_list)
    CBISchedule.objects.bulk_create(cbi_schedule_list)

    print('Done migration.')
                

if __name__ == '__main__':
    migrate_data()
