# Generated by Django 4.2 on 2023-04-27 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_cbi_candidate_alter_hiring_candidate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescreeningsubmission',
            name='prescreening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.prescreening'),
        ),
    ]
