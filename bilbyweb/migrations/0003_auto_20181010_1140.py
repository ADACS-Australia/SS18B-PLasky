# Generated by Django 2.0.7 on 2018-10-10 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilbyweb', '0002_auto_20181005_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='extra_status',
            field=models.CharField(choices=[('none', 'None'), ('public', 'Public')], default='none', max_length=20),
        ),
    ]