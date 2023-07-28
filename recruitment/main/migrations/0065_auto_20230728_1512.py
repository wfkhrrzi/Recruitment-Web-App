# Generated by Django 3.2.9 on 2023-07-28 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_merge_20230728_1512'),
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
            name='email',
            field=models.EmailField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='highest_education',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='main_skills',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='recent_emp',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='recent_role',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='referral_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
