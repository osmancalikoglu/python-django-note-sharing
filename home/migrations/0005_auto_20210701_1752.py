# Generated by Django 3.2.4 on 2021-07-01 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='facebook',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='instagram',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
