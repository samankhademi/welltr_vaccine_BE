# Generated by Django 3.2.5 on 2022-01-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20220111_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaymenttransaction',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'CREATED'), ('FAILED', 'FAILED'), ('UNKNOWN', 'UNKNOWN'), ('SUCCESS', 'SUCCESS')], default='IN_PROGRESS', max_length=50, verbose_name='payment status'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'CREATED'), ('FAILED', 'FAILED'), ('UNKNOWN', 'UNKNOWN'), ('SUCCESS', 'SUCCESS')], default='IN_PROGRESS', max_length=50, verbose_name='payment status'),
        ),
    ]