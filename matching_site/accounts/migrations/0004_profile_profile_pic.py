# Generated by Django 2.1.2 on 2018-11-24 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181123_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
