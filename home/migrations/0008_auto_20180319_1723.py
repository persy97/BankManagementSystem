# Generated by Django 2.0.2 on 2018-03-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20180319_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='tri',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='requestedaddress',
            field=models.CharField(default='a', max_length=150),
        ),
    ]