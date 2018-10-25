# Generated by Django 2.0.7 on 2018-10-05 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilbyweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='status',
        ),
        migrations.AddField(
            model_name='job',
            name='extra_status',
            field=models.CharField(choices=[('none', 'None'), ('saved', 'Saved'), ('deleted', 'Deleted'), ('public', 'Public')], default='none', max_length=20),
        ),
    ]