# Generated by Django 3.2.4 on 2021-06-28 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_rename_level_category_mptt_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
