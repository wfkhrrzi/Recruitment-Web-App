# Generated by Django 4.2 on 2023-04-27 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_initialscreeningevaluation_last_modified_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialscreeningevaluation',
            name='is_proceed',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='initialscreeningevaluation',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.status'),
        ),
    ]