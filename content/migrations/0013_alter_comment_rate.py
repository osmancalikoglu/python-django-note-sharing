# Generated by Django 3.2.4 on 2021-07-01 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_auto_20210701_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
