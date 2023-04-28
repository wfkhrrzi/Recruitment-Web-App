# Generated by Django 4.2 on 2023-04-27 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_status_codename'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescreening',
            name='assessment_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescreening_assessment_status', to='main.status'),
        ),
        migrations.AlterField(
            model_name='prescreening',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescreening_status', to='main.status'),
        ),
    ]
