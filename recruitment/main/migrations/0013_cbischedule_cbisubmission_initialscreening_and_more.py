# Generated by Django 4.2 on 2023-04-21 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_candidate_hr_remarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='CBISchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('remarks', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CBISubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission', models.FileField(upload_to=main.models.Submission.upload_directory)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InitialScreening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(null=True)),
                ('selection_date', models.DateField(null=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InitialScreeningEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescreening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrescreeningSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission', models.FileField(upload_to=main.models.Submission.upload_directory)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('initial_screening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.initialscreening')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='Joining',
            new_name='Hiring',
        ),
        migrations.RemoveField(
            model_name='screening',
            name='candidate',
        ),
        migrations.RemoveField(
            model_name='screening',
            name='selection_status',
        ),
        migrations.RemoveField(
            model_name='screeningevaluation',
            name='screening',
        ),
        migrations.RemoveField(
            model_name='screeningevaluation',
            name='status',
        ),
        migrations.RemoveField(
            model_name='screeningevaluation',
            name='user',
        ),
        migrations.RemoveField(
            model_name='screeningsubmission',
            name='screening',
        ),
        migrations.RenameField(
            model_name='cbi',
            old_name='feedback',
            new_name='remarks',
        ),
        migrations.RemoveField(
            model_name='cbi',
            name='assessor1',
        ),
        migrations.RemoveField(
            model_name='cbi',
            name='assessor2',
        ),
        migrations.AddField(
            model_name='cbi',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cbi',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cbi_user_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cbi',
            name='last_modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='cbi',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cbi_user_last_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.empcategory'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.source'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.usercategory'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_privilege',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.userprivilege'),
        ),
        migrations.DeleteModel(
            name='AssessorAvailability',
        ),
        migrations.DeleteModel(
            name='Screening',
        ),
        migrations.DeleteModel(
            name='ScreeningEvaluation',
        ),
        migrations.DeleteModel(
            name='ScreeningSubmission',
        ),
        migrations.AddField(
            model_name='prescreening',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.candidate'),
        ),
        migrations.AddField(
            model_name='prescreening',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescreening_user_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescreening',
            name='initial_screening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.initialscreening'),
        ),
        migrations.AddField(
            model_name='prescreening',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescreening_user_last_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescreening',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.status'),
        ),
        migrations.AddField(
            model_name='prescreening',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='initialscreeningevaluation',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='initscreening_user_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='initialscreeningevaluation',
            name='initial_screening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.initialscreening'),
        ),
        migrations.AddField(
            model_name='initialscreeningevaluation',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.status'),
        ),
        migrations.AddField(
            model_name='initialscreeningevaluation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='initscreening_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='initialscreening',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.candidate'),
        ),
        migrations.AddField(
            model_name='initialscreening',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='initialscreening',
            name='selection_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.status'),
        ),
        migrations.AddField(
            model_name='cbisubmission',
            name='cbi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cbi'),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='assessor1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user1_CBISchedule', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='assessor1_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user1_status', to='main.status'),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='assessor2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user2_CBISchedule', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='assessor2_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user2_status', to='main.status'),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='assessor3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user3_CBISchedule', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='assessor3_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user3_status', to='main.status'),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='cbi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cbi'),
        ),
        migrations.AddField(
            model_name='cbischedule',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.status'),
        ),
    ]