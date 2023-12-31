# Generated by Django 3.2.5 on 2022-01-06 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0013_auto_20211003_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='is_used_coupon',
            field=models.BooleanField(default=False, verbose_name='is order used coupon ?'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_used_coupon',
            field=models.BooleanField(default=False, verbose_name='is order used coupon ?'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('WAITING_FOR_DATA_SUBMISSION', 'waiting for data submisson'), ('FULL PAID', 'full paid'), ('PAID 20 PERCENT', 'paid 20 percent'), ('WAITING_FOR_SETTING_FIRST_DOSE', 'Waiting for setting first dose'), ('WAITING_FOR_PAY', 'Waiting for pay'), ('WAITING_FOR_RECEIVING_FIRST_DOSE', 'Waiting for receiving first dose'), ('WAITING_FOR_SETTING_SECOND_DOSE', 'Waiting for setting second dose'), ('WAITING_FOR_RECEIVING_SECOND_DOSE', 'Waiting for receiving second dose'), ('DONE', 'Done')], default='OPEN', max_length=50, verbose_name='order status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('WAITING_FOR_DATA_SUBMISSION', 'waiting for data submisson'), ('FULL PAID', 'full paid'), ('PAID 20 PERCENT', 'paid 20 percent'), ('WAITING_FOR_SETTING_FIRST_DOSE', 'Waiting for setting first dose'), ('WAITING_FOR_PAY', 'Waiting for pay'), ('WAITING_FOR_RECEIVING_FIRST_DOSE', 'Waiting for receiving first dose'), ('WAITING_FOR_SETTING_SECOND_DOSE', 'Waiting for setting second dose'), ('WAITING_FOR_RECEIVING_SECOND_DOSE', 'Waiting for receiving second dose'), ('DONE', 'Done')], default='OPEN', max_length=50, verbose_name='order status'),
        ),
        migrations.CreateModel(
            name='HistoricalCoupon',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='updated at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('pin', models.CharField(blank=True, max_length=50, null=True, verbose_name='coupon pin')),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('USED', 'USED'), ('DISABLED', 'DISABLED')], default='AVAILABLE', max_length=50, verbose_name='coupon status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='order.order', verbose_name='related order')),
            ],
            options={
                'verbose_name': 'historical coupon',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='updated at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('pin', models.CharField(blank=True, max_length=50, null=True, verbose_name='coupon pin')),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('USED', 'USED'), ('DISABLED', 'DISABLED')], default='AVAILABLE', max_length=50, verbose_name='coupon status')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupons', to='order.order', verbose_name='related order')),
            ],
            options={
                'verbose_name': 'coupon',
                'verbose_name_plural': 'coupon',
            },
        ),
    ]
