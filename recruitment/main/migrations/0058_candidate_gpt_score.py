# Generated by Django 4.2 on 2023-07-04 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_parserconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='gpt_score',
            field=models.FloatField(null=True),
        ),
    ]
