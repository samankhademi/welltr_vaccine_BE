# Generated by Django 3.2.5 on 2021-07-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaymenttransaction',
            name='transaction_response',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='transaction log'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='transaction_response',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='transaction log'),
        ),
    ]
