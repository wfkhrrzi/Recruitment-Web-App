# Generated by Django 3.2.9 on 2023-05-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_cbi_is_active_prescreening_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='ds_background',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='ds_skills',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='highest_education',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='main_skills',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone_number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='recent_emp',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='recent_role',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='referral_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='users',
            name='alias',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
