# Generated by Django 3.2.5 on 2021-08-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20210804_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone number'),
        ),
        migrations.AddField(
            model_name='historicalexchange',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone number'),
        ),
    ]
