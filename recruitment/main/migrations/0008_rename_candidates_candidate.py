# Generated by Django 4.2 on 2023-04-14 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_screeningfiles_screeningsubmission'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Candidates',
            new_name='Candidate',
        ),
    ]
