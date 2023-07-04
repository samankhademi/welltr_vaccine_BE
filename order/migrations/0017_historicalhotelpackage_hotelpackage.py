# Generated by Django 3.2.5 on 2022-01-08 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0016_auto_20220106_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='updated at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('total_person', models.IntegerField(default=1, verbose_name='total person')),
                ('hotel_name', models.CharField(max_length=250, verbose_name='hotel name')),
                ('nights_num', models.IntegerField(default=1, verbose_name='number of nights')),
                ('price', models.FloatField(default=0, verbose_name='package price')),
                ('desc_fa', models.TextField(blank=True, null=True, verbose_name='farsi description')),
                ('desc_en', models.TextField(blank=True, null=True, verbose_name='english description')),
                ('desc_tr', models.TextField(blank=True, null=True, verbose_name='turkish description')),
                ('address_fa', models.TextField(blank=True, null=True, verbose_name='farsi description')),
                ('address_en', models.TextField(blank=True, null=True, verbose_name='english description')),
                ('address_tr', models.TextField(blank=True, null=True, verbose_name='turkish description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalHotelPackage',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='updated at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('total_person', models.IntegerField(default=1, verbose_name='total person')),
                ('hotel_name', models.CharField(max_length=250, verbose_name='hotel name')),
                ('nights_num', models.IntegerField(default=1, verbose_name='number of nights')),
                ('price', models.FloatField(default=0, verbose_name='package price')),
                ('desc_fa', models.TextField(blank=True, null=True, verbose_name='farsi description')),
                ('desc_en', models.TextField(blank=True, null=True, verbose_name='english description')),
                ('desc_tr', models.TextField(blank=True, null=True, verbose_name='turkish description')),
                ('address_fa', models.TextField(blank=True, null=True, verbose_name='farsi description')),
                ('address_en', models.TextField(blank=True, null=True, verbose_name='english description')),
                ('address_tr', models.TextField(blank=True, null=True, verbose_name='turkish description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical hotel package',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
