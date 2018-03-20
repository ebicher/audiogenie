# Generated by Django 2.0.2 on 2018-02-27 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audiogenie', '0007_auto_20180227_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='track_file',
            field=models.FileField(null=True, upload_to='media/tracks/'),
        ),
        migrations.AlterField(
            model_name='track',
            name='creation_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='track',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audiogenie.Project'),
        ),
    ]
