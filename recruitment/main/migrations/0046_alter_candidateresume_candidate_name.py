# Generated by Django 4.2 on 2023-05-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_remove_candidateresume_referral_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateresume',
            name='candidate_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]