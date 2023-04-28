# Generated by Django 4.2 on 2023-04-27 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_cbisubmission_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbisubmission',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='cbisubmission',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cbisubmission_user_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescreeningsubmission',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='prescreeningsubmission',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescreeningsubmission_user_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
