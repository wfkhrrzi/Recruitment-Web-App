# Generated by Django 4.2 on 2023-05-26 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_alter_candidateresume_candidate_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateresume',
            name='is_parsed',
            field=models.BooleanField(default=False),
        ),
    ]
