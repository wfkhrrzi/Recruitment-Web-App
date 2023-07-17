import pandas as pd
import django
import os
import pandas as pd
from io import BytesIO
from datetime import datetime
import random
from tqdm import tqdm

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")
django.setup()

# Import your Django models
from main.models import Candidate,Source,EmpCategory,Status,CandidateResume,Nationality,InitialScreening,InitialScreeningEvaluation,Users,Prescreening,CBI

def migrate_data():

    print('Start migration...')

    directory = 'C://Users//wanfakhrurrazi.wanaz//PETRONAS//Khairina Ibrahim (DS DIGITAL) - New Resumes'
    df = pd.read_csv('C://PET DIG Projects//LOCAL Recruitment//Existing Candidates MIGRATION//new_recruitment_preprocessed.csv',)

    # Retrieve files in the directory
    files = os.listdir(directory)

    # Iterate over the candidates
    candidates_list = []
    initialscreening_list = []
    initialscreening_eval_list = []
    prescreening_list = []
    cbi_list = []
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
            gpt_score=random.randint(1, 100),
            date = date,
            referral_name = row['Referred By'],
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
        
        is_status = Status.objects.get(codename='initscreening:selected' if is_proceed == True else 'initscreening:not selected' if is_proceed == False else 'initscreening:pending')
        is_hm_status = Status.objects.get(codename='initscreening:selected' if is_hm_proceed else 'initscreening:not selected') if is_hm_proceed != None else None

        initialscreening = InitialScreening(
            candidate=candidate,
            hm_status=is_hm_status,
            is_hm_proceed=is_hm_proceed,
            is_proceed=is_proceed,
            status=is_status,
            date_selected=datetime.strptime(row['Selection Date'], '%Y-%m-%d').date() if pd.isnull(row['Selection Date']) != True else None,
            remarks=row['Comment/Remarks'] if pd.isnull(row['Comment/Remarks']) != True else None,
        )

        candidate.overall_status = Status.objects.get(codename="initscreening:ongoing" if is_proceed else "initscreening:not selected" )

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
        cbi.status = Status.objects.get(codename='cbi:pending schedule')

        if pd.isnull(row['Selection']):
            
            candidate.overall_status = initialscreening.status
        
        elif not pd.isnull(row['Remark']) and 'salary' in row['Remark'].lower():
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            if row['Joining Status'] == 'Recruited':
                cbi.is_proceed = True
                cbi.status = Status.objects.get(codename='cbi:proceed')
            else:
                cbi.is_proceed = False
                cbi.status = Status.objects.get(codename='cbi:not proceed')

            candidate.overall_status = cbi.status

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)

        elif not pd.isnull(row['Remark']) and 'screen' in row['Remark'].lower() and 'interview' in row['Remark'].lower():

            prescreening.is_proceed = False
            prescreening.status = Status.objects.get(codename='prescreening:not proceed')
            candidate.overall_status = prescreening.status

            prescreening_list.append(prescreening)

        elif not pd.isnull(row['Remark']) and 'cbi result' in row['Remark'].lower():
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            cbi.status = Status.objects.get(codename='cbi:pending result')
            candidate.overall_status = cbi.status

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)

        elif row['Joining Status'] == 'Pending CBI':
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            cbi.status = Status.objects.get(codename='cbi:pending schedule')
            candidate.overall_status = cbi.status

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)

        elif row['Joining Status'] == 'Pending HKR Result':
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')

            cbi.status = Status.objects.get(codename='cbi:pending result')
            candidate.overall_status = cbi.status

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)

        elif row['Joining Status'] in ('Pending Pre screen','Hold','Pending'):
            prescreening.status = Status.objects.get(codename='prescreening:pending')
            candidate.overall_status = prescreening.status

            prescreening_list.append(prescreening)

        elif row['Joining Status'] in ('Not Recommended','Withdraw'):
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')
            cbi.is_proceed = False
            cbi.status = Status.objects.get(codename='cbi:not proceed')
            candidate.overall_status = cbi.status

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)

        elif row['Joining Status'] in ('Recruited','Declined ','Pending SP'):
            prescreening.is_proceed = True
            prescreening.status = Status.objects.get(codename='prescreening:proceed')
            cbi.is_proceed = True
            cbi.status = Status.objects.get(codename='cbi:proceed')
            candidate.overall_status = cbi.status

            prescreening_list.append(prescreening)
            cbi_list.append(cbi)


    # Bulk create instances
    Candidate.objects.bulk_create(candidates_list)
    InitialScreening.objects.bulk_create(initialscreening_list)
    InitialScreeningEvaluation.objects.bulk_create(initialscreening_eval_list)
    Prescreening.objects.bulk_create(prescreening_list)
    CBI.objects.bulk_create(cbi_list)

    print('Done migration.')
                

if __name__ == '__main__':
    migrate_data()
