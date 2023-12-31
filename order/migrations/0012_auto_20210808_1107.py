# Generated by Django 3.2.5 on 2021-08-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20210808_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalvaccinecenter',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='historicalvaccinecenter',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vaccinecenter',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='vaccinecenter',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
