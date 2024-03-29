# Generated by Django 4.2 on 2023-04-13 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assessoravailability',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='candidates',
            old_name='categoryId',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='candidates',
            old_name='last_modified_byId',
            new_name='last_modified_by',
        ),
        migrations.RenameField(
            model_name='candidates',
            old_name='sourceId',
            new_name='source',
        ),
        migrations.RenameField(
            model_name='cbi',
            old_name='assessor1_id',
            new_name='assessor1',
        ),
        migrations.RenameField(
            model_name='cbi',
            old_name='assessor2_id',
            new_name='assessor2',
        ),
        migrations.RenameField(
            model_name='cbi',
            old_name='candidateId',
            new_name='candidate',
        ),
        migrations.RenameField(
            model_name='cbi',
            old_name='statusId',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='joining',
            old_name='candidateId',
            new_name='candidate',
        ),
        migrations.RenameField(
            model_name='joining',
            old_name='statusId',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='screening',
            old_name='candidateId',
            new_name='candidate',
        ),
        migrations.RenameField(
            model_name='screening',
            old_name='selectionStatusId',
            new_name='selectionStatus',
        ),
        migrations.RenameField(
            model_name='screeningevaluation',
            old_name='screeningId',
            new_name='screening',
        ),
        migrations.RenameField(
            model_name='screeningevaluation',
            old_name='statusId',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='screeningevaluation',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='userCategoryId',
            new_name='user_category',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='userPrivilegeId',
            new_name='user_privilege',
        ),
    ]
