# Generated by Django 3.2.5 on 2021-07-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20210724_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='passport_image',
            field=models.ImageField(blank=True, null=True, upload_to='passports', verbose_name='passport image'),
        ),
    ]
