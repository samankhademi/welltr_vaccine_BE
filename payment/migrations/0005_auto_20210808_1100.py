# Generated by Django 3.2.5 on 2021-08-08 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20210804_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaymenttransaction',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='historicalpaymenttransaction',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
