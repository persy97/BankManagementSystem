# Generated by Django 2.0.2 on 2018-03-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20180318_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='cheque',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='requestedaddress',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='stopcheque',
            field=models.BooleanField(default=False),
        ),
    ]