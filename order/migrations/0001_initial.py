# Generated by Django 3.2.5 on 2021-07-17 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
            options={
                'verbose_name': 'vaccine center',
                'verbose_name_plural': 'vaccine centers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('PAID', 'Paid'), ('WAITING_FOR_FIRST_DOSE', 'Waiting for first dose'), ('WAITING_FOR_SECOND_DOSE', 'Waiting for second dose'), ('DONE', 'Done')], default='OPEN', max_length=50, verbose_name='order status')),
                ('vaccine_type', models.CharField(max_length=50, verbose_name='vaccine type')),
                ('dose1_flight_number', models.CharField(max_length=50, verbose_name='dose 1 flight number')),
                ('transport_company_name', models.CharField(max_length=50, verbose_name='dose 1 transportation company name')),
                ('arrival_date', models.DateField(verbose_name='dose 1 arrival date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='related user')),
                ('vaccine_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='order.vaccinecenter', verbose_name='vaccine center')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='HistoricalVaccineCenter',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='updated at')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical vaccine center',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='updated at')),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('PAID', 'Paid'), ('WAITING_FOR_FIRST_DOSE', 'Waiting for first dose'), ('WAITING_FOR_SECOND_DOSE', 'Waiting for second dose'), ('DONE', 'Done')], default='OPEN', max_length=50, verbose_name='order status')),
                ('vaccine_type', models.CharField(max_length=50, verbose_name='vaccine type')),
                ('dose1_flight_number', models.CharField(max_length=50, verbose_name='dose 1 flight number')),
                ('transport_company_name', models.CharField(max_length=50, verbose_name='dose 1 transportation company name')),
                ('arrival_date', models.DateField(verbose_name='dose 1 arrival date')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='related user')),
                ('vaccine_center', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='order.vaccinecenter', verbose_name='vaccine center')),
            ],
            options={
                'verbose_name': 'historical order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
