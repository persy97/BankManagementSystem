# Generated by Django 2.0.2 on 2018-03-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_transactions_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='accountno',
            field=models.IntegerField(default=0),
        ),
    ]
