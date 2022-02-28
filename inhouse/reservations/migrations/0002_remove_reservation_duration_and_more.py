# Generated by Django 4.0.2 on 2022-02-23 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boardmanlab', '0002_helpsession_time'),
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='helper',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='student',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='topic',
        ),
        migrations.AddField(
            model_name='reservation',
            name='helpSession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boardmanlab.helpsession'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]