# Generated by Django 3.2.5 on 2021-08-04 10:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='exchange name')),
                ('state', models.CharField(max_length=50, verbose_name='exchange state, city')),
                ('address', models.CharField(max_length=100, verbose_name='exchange address')),
                ('users', models.ManyToManyField(blank=True, null=True, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='exchange users')),
            ],
        ),
    ]