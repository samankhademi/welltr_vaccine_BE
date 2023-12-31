# Generated by Django 3.2.5 on 2021-08-04 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20210804_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalvaccinecenter',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='historicalvaccinecenter',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vaccinecenter',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='vaccinecenter',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
