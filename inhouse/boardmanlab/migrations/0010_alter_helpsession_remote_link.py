# Generated by Django 4.0.3 on 2022-04-05 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardmanlab', '0009_alter_helpsession_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpsession',
            name='remote_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]