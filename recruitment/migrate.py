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
from main.models import Candidate,Source,EmpCategory,CandidateResume

def migrate_data():

    directory = 'C://Users//wanfakhrurrazi.wanaz//PETRONAS//Khairina Ibrahim (DS DIGITAL) - New Resumes'
    df = pd.read_csv('C://PET DIG Projects//LOCAL Recruitment//Existing Candidates MIGRATION//new_recruitment_preprocessed.csv',)

    # Retrieve files in the directory
    files = os.listdir(directory)

    # Iterate over the files
    candidates_list = []
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
            source = source,
            category = category,
            date = date,
            referral_name = row['Referred By']
        )

        for file in files:
            if f"resume_{row['id']}.pdf" in file:
                resume = CandidateResume(submission=open(directory+'/'+file,'rb').read(), filename=file)
                resume.save()

                candidate.candidate_resume = resume

        candidates_list.append(candidate)

    # print(candidates_list)
    Candidate.objects.bulk_create(candidates_list)

    print('Done migration.')
                

if __name__ == '__main__':
    migrate_data()
