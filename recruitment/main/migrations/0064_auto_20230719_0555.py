# Generated by Django 3.2.9 on 2023-07-18 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0063_merge_20230718_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='CGPA',
            field=models.CharField(max_length=255, null=True),
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
        migrations.AlterField(
            model_name='candidate',
            name='years_exp',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
