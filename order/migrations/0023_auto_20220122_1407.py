# Generated by Django 3.2.5 on 2022-01-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_auto_20220113_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='usdt_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='usdt payment address'),
        ),
        migrations.AddField(
            model_name='order',
            name='usdt_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='usdt payment address'),
        ),
    ]