# Generated by Django 4.2 on 2023-05-29 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_alter_candidate_cgpa_alter_candidate_cv_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='candidate_resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.candidateresume'),
        ),
    ]
