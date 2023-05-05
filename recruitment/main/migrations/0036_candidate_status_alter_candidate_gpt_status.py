# Generated by Django 4.2 on 2023-05-04 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_cbischedule_created_at_cbischedule_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='candidates_overall_status', to='main.status'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='gpt_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='candidates_gpt_status', to='main.status'),
        ),
    ]
