# Generated by Django 3.2 on 2022-12-11 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20221210_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='paperId',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
