# Generated by Django 4.2 on 2023-04-27 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_cbisubmission_deleted_at_cbisubmission_deleted_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]