# Generated by Django 2.2.1 on 2019-05-09 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_comment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
