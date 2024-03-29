# Generated by Django 4.2 on 2023-05-12 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_users_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialscreening',
            name='hm_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initialscreening_hm_status', to='main.status'),
        ),
        migrations.AddField(
            model_name='initialscreening',
            name='is_hm_proceed',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='initialscreening',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initialscreening_final_status', to='main.status'),
        ),
        migrations.AlterField(
            model_name='initialscreeningevaluation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='initialscreeningevaluation_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
