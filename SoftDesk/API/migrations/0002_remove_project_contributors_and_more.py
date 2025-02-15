# Generated by Django 5.0.4 on 2024-04-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='project',
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ManyToManyField(related_name='contributors', to='API.project'),
        ),
    ]
