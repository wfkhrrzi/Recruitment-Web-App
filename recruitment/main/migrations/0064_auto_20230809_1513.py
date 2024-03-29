# Generated by Django 3.2.9 on 2023-08-09 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0063_alter_candidate_cgpa_alter_candidate_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='alias',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
    ]
