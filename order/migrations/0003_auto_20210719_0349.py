# Generated by Django 3.2.5 on 2021-07-19 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210719_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('WAITING_FOR_DATA_SUBMISSION', 'waiting for data submisson'), ('FULL PAID', 'full paid'), ('PAID 20 PERCENT', 'paid 20 percent'), ('WAITING_FOR_SETTING_FIRST_DOSE', 'Waiting for setting first dose'), ('WAITING_FOR_RECEIVING_FIRST_DOSE', 'Waiting for receiving first dose'), ('WAITING_FOR_SETTING_SECOND_DOSE', 'Waiting for setting second dose'), ('WAITING_FOR_RECEIVING_SECOND_DOSE', 'Waiting for receiving second dose'), ('DONE', 'Done')], default='OPEN', max_length=50, verbose_name='order status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('WAITING_FOR_DATA_SUBMISSION', 'waiting for data submisson'), ('FULL PAID', 'full paid'), ('PAID 20 PERCENT', 'paid 20 percent'), ('WAITING_FOR_SETTING_FIRST_DOSE', 'Waiting for setting first dose'), ('WAITING_FOR_RECEIVING_FIRST_DOSE', 'Waiting for receiving first dose'), ('WAITING_FOR_SETTING_SECOND_DOSE', 'Waiting for setting second dose'), ('WAITING_FOR_RECEIVING_SECOND_DOSE', 'Waiting for receiving second dose'), ('DONE', 'Done')], default='OPEN', max_length=50, verbose_name='order status'),
        ),
    ]
