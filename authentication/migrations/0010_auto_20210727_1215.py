# Generated by Django 3.2.5 on 2021-07-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_alter_person_passport_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperson',
            name='national_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='national id'),
        ),
        migrations.AlterField(
            model_name='person',
            name='national_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='national id'),
        ),
    ]