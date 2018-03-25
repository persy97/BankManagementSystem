from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomerDetails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    transpass = models.CharField(max_length=10, default=1)
    requestedaddress = models.CharField(max_length=150, default='')
    cheque = models.BooleanField(default=False)
    stopcheque = models.BooleanField(default=False)
    tri = models.IntegerField(default=3)


class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accountno = models.IntegerField(default=0, primary_key=True)
    balance = models.IntegerField(default=0)


class Transactions(models.Model):
    accountno = models.IntegerField(default=0)
    to = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=1, default='D')
    date = models.DateTimeField(auto_now=True)
