# Generated by Django 2.0.7 on 2018-09-14 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tupakweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='prior',
            unique_together={('job', 'name')},
        ),
    ]
