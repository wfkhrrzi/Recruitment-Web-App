# Generated by Django 4.2 on 2023-06-20 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_nationality_candidate_nationality'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParserConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('job_description', models.TextField()),
            ],
        ),
    ]
