# Generated by Django 4.2 on 2023-04-15 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_candidate_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='screeningsubmission',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
