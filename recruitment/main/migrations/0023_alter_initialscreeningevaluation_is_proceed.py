# Generated by Django 4.2 on 2023-04-27 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_initialscreeningevaluation_is_proceed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialscreeningevaluation',
            name='is_proceed',
            field=models.BooleanField(),
        ),
    ]
