# Generated by Django 4.2.1 on 2023-07-18 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_alter_candidate_years_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='ds_background',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='ds_skills',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='main_skills',
            field=models.TextField(null=True),
        ),
    ]
