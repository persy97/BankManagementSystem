# Generated by Django 2.0.2 on 2018-03-17 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='transpass',
            field=models.CharField(default=1, max_length=10),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]