# Generated by Django 4.2 on 2023-06-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_alter_candidateresume_submission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateresume',
            name='filename',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='cbisubmission',
            name='filename',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='prescreeningsubmission',
            name='filename',
            field=models.CharField(default='', max_length=200),
        ),
    ]
