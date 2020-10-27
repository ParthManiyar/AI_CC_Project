# Generated by Django 2.2.16 on 2020-10-13 06:39

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slip',
            fields=[
                ('Account_Number', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^\\d{1,10}$'), django.core.validators.MinLengthValidator(10)])),
                ('Image_Path', models.FilePathField()),
                ('Current_Date', models.DateTimeField(default=datetime.datetime(2020, 10, 13, 6, 39, 3, 732194, tzinfo=utc))),
                ('Account_Holder_Name', models.CharField(max_length=200)),
                ('Bank_Name', models.CharField(max_length=200)),
            ],
        ),
    ]