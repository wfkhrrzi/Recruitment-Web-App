# Generated by Django 4.2 on 2023-04-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_screeningsubmission_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
