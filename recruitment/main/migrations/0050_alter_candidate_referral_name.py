# Generated by Django 4.2 on 2023-05-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_candidate_candidate_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='referral_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
