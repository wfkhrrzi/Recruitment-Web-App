# Generated by Django 4.2 on 2023-06-01 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_alter_candidate_referral_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateresume',
            name='is_parsing',
            field=models.BooleanField(default=False),
        ),
    ]
