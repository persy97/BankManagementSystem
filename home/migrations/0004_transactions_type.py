# Generated by Django 2.0.2 on 2018-03-18 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20180317_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='type',
            field=models.CharField(default='D', max_length=1),
        ),
    ]
