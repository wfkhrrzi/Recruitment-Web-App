import pandas as pd
import django
import os
import pandas as pd
from io import BytesIO
from datetime import datetime

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")
django.setup()

# Import your Django models
from main.models import Candidate,Source,EmpCategory,Status,CandidateResume,Nationality,InitialScreening,InitialScreeningEvaluation,Users

def migrate_data():

    print('Start migration...')

    directory = 'C://Users//wanfakhrurrazi.wanaz//PETRONAS//Khairina Ibrahim (DS DIGITAL) - New Resumes'
    df = pd.read_csv('C://PET DIG Projects//LOCAL Recruitment//Existing Candidates MIGRATION//new_recruitment_preprocessed.csv',)

    # Retrieve files in the directory
    files = os.listdir(directory)

    # Iterate over the files
    candidates_list = []
    initialscreening_list = []
    initialscreening_eval_list = []
    for index, row in df.iterrows():

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
        )

        for file in files:
            if f"resume_{row['id']}.pdf" in file:
                resume = CandidateResume(submission=open(directory+'/'+file,'rb').read(), filename=file, is_parsed=True)
                resume.save()
                
                candidate.candidate_resume = resume

                break


        is_proceed = bool(row['Selection']) if not pd.isnull(row['Selection']) else None
        is_hm_proceed = None if is_proceed == None else False if row[7:20].isna().all() and is_proceed else True
        
        is_status = Status.objects.get(codename='initscreening:selected' if is_proceed else 'initscreening:not selected') if is_proceed != None else None
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

    # print(candidates_list)
    Candidate.objects.bulk_create(candidates_list)
    InitialScreening.objects.bulk_create(initialscreening_list)
    InitialScreeningEvaluation.objects.bulk_create(initialscreening_eval_list)


    print('Done migration.')
                

if __name__ == '__main__':
    migrate_data()
