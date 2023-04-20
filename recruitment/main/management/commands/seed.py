from main.models import *
from django.core.management.base import BaseCommand, CommandParser
from main.seeder.factories import *
from django.db import connection
import warnings

warnings.filterwarnings('ignore')


MODE_REFRESH = 'refresh'
""" Clear all data and create new ones"""

MODE_CLEAR = 'clear'
""" Clear all data and do not create any object """

MODE_SEED = 'seed'
""" Add another instances """

lst_models = [Status,EmpCategory,Source,Users,Candidate,Screening,ScreeningSubmission]

class Command(BaseCommand):
    help = "Seed database for testing and development"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.run_seed(options['mode'])

    def clear_data(self):
        """Deletes all the table data"""
        self.stdout.write("Deleting all instances from all tables")
        
        cursor = connection.cursor()
        
        for model in lst_models:
            model_name = model.__name__.lower()

            #clear data
            model.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'All instances from table "main_{model_name}" are deleted.'))

            #reset sequences
            cursor.execute(f'UPDATE sqlite_sequence SET seq = 0 WHERE sqlite_sequence.name = "main_{model_name}"')
            row = cursor.execute(f'SELECT seq FROM sqlite_sequence WHERE sqlite_sequence.name = "main_{model_name}"').fetchone()

            if row:
                if row[0] == 0:
                    self.stdout.write(self.style.SUCCESS(f'Sequence for table "main_{model_name}" reset to {str(row[0])}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Sequence for table "main_{model_name}" failed to reset. Remains to {str(row[0])}'))
        
        
    def run_seed(self, mode):
        """ Seed database based on mode

        :param mode: refresh / clear 
        :return:
        """
        # Clear data from tables
        if mode == MODE_REFRESH:
            self.clear_data()
        if mode == MODE_CLEAR:
            return
        
        #run factories
        self.stdout.write('Seeding database...')

        # status, source, emp category
        EmpCategoryFactory.create_batch(3)
        SourceFactory.create_batch(3)
        StatusFactory.create_batch(3)

        # users
        UsersFactory.create_batch(3)
        AdminFactory.create_batch(2)

        # candidates
        CandidateFactory.create_batch(30)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))

            
        


    