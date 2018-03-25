from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('profile')
            else:
                form = UserCreationForm()
                return render(request, 'registration/register.html', {'form': form, 'error': 'Form is invalid'})
        except:
            form = UserCreationForm()
            return render(request, 'registration/register.html', {'form': form, 'error': 'Invalid Username/Password'})


    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)


def profile(request):
    if request.user.is_authenticated:
        try:
            ad = CustomerDetails.objects.get(user=request.user)
        except:
            ad = CustomerDetails.objects.get_or_create(user=request.user)
        adr = Accounts.objects.filter(user=request.user)
        summ = 0
        for i in adr:
            summ = summ + i.balance

        context = {
            'address': ad,
            'balance': summ,
        }
        return render(request, 'profile/profile.html', context)
    elif request.method == 'POST':
        ad = CustomerDetails.objects.get(user=request.user)
        adr = Accounts.objects.filter(user=request.user)
        summ=0
        for i in adr:
            summ = summ + i.balance

        context = {
            'address': ad,
            'balance': summ,
        }
        return render(request, 'profile/profile.html',  context)
    else:
        return redirect('home')


def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    elif request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            try:
                usr = User.objects.get(username=request.POST.get('username'))
            except:
                form = UserCreationForm()
                return render(request, 'homepage/homepage.html', {'form': form, 'message': 'Invalid Username/Password'})
            us = CustomerDetails.objects.get(user=usr)
            us.tri = us.tri + 1
            us.save()
            if us.tri > 2:
                usr.is_active = False
                usr.save()
                form = UserCreationForm()
                return render(request, 'homepage/homepage.html',
                                  {'form': form, 'message': 'You have exceeded the maximum '
                                                            'number of login attempts. '
                                                            'Please contact the bank. '})
            form = UserCreationForm()
            return render(request, 'homepage/homepage.html', {'form': form, 'message': 'Invalid Username/Password'})
        else:
            if user.is_active:
                login(request, user)
                usr = User.objects.get(username=request.POST.get('username'))
                us = CustomerDetails.objects.get(user=usr)
                us.tri = 0
                us.save()
                return redirect('profile')
            else:
                form = UserCreationForm()
                return render(request, 'homepage/homepage.html', {'form': form, 'message': 'You have exceeded the '
                                                                                           'maximum number '
                                                                                           'of login attempts. '
                                                                                           'Please Contact the Bank.'})


    elif request.method=='GET':
        form=UserCreationForm()
        return render(request,'homepage/homepage.html',{'form': form})



def send(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            c = Accounts.objects.filter(user=request.user)
            context = {'c': c, }
            return render(request, 'send/send.html', context)
        if request.method == 'POST':
            tpass = request.POST.get('transpas')
            ttpass = CustomerDetails.objects.get(user=request.user)
            tttpass = ttpass.transpass
            if not tpass == tttpass:
                c = Accounts.objects.filter(user=request.user)
                context = {'c': c, 'error_message': 'Invalid Transaction Password', }
                return render(request, 'send/send.html', context)
            recieversaccount = request.POST.get('recacc')
            sendersaccount = request.POST.get('senacc')
            amountadded = request.POST.get('amnt')
            saccount = Accounts.objects.get(accountno=int(sendersaccount))
            if saccount.balance < int(amountadded):
                c = Accounts.objects.filter(user=request.user)
                context = {'c': c, 'error_message': 'Insufficient Balance in the selected account. '
                                                    'Please select another account or add money in the '
                                                    'selected account', }
                return render(request, 'send/send.html', context)
            try:
                raccount = Accounts.objects.get(accountno=int(recieversaccount))
            except:
                c = Accounts.objects.filter(user=request.user)
                context = {'c': c, 'error_message': 'No Account linked with the entered Account Number, '
                                                    'Please try again', }
                return render(request, 'send/send.html', context)
            ssaccount = Accounts.objects.get(accountno=int(sendersaccount))
            ssaccount.balance = ssaccount.balance - int(amountadded)
            ssaccount.save()
            rraccount = Accounts.objects.get(accountno=int(recieversaccount))
            rraccount.balance = rraccount.balance + int(amountadded)

            rraccount.save()
            qwerty = Transactions(accountno=int(sendersaccount), to=int(recieversaccount),
                                  amount=int(amountadded), type='D')
            qwerty.save()
            ad = CustomerDetails.objects.get(user=request.user)
            adr = Accounts.objects.filter(user=request.user)
            summ = 0
            for i in adr:
                summ = summ + i.balance

            context = {
                'address': ad,
                'balance': summ,
                'message': 'Successfully Transferred',
            }
            return render(request, 'profile/profile.html', context)

    elif not request.user.is_authenticated:
        return redirect('home')


def history(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            acnt = int(request.POST.get('acntno'))
            aa = reversed(Transactions.objects.filter(accountno=acnt))
            daa = reversed(Transactions.objects.filter(to=acnt))
            currentuser = Accounts.objects.filter(user=request.user)
            return render(request, 'history/history.html', {'currentuser': currentuser, 'aa': aa,'daa':daa, })
        elif request.method=='GET':
            currentuser = Accounts.objects.filter(user=request.user)
            return render(request, 'history/history.html', {'currentuser': currentuser,})


def logoutt(request):
    logout(request)
    return redirect('home')


def changepass(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            context = {
                'message': 'Your Password is successfully changed',
            }
            return render(request, 'change_password.html', context)
        else:
            context = {
                'messagess': 'Please correct the errors below:',
            }
            return render(request, 'change_password.html', context)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html')

def change(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            adrt = CustomerDetails.objects.get(user=request.user)
            return render(request, 'changeaddress.html', {'adrt': adrt, })
        if request.method == 'POST':
            cd = CustomerDetails.objects.get(user=request.user)
            cd.requestedaddress = request.POST.get('addrs')
            cd.save()
            ad = CustomerDetails.objects.get(user=request.user)
            adr = Accounts.objects.filter(user=request.user)
            summ = 0
            for i in adr:
                summ = summ + i.balance

            context = {
                'address': ad,
                'balance': summ,
                'messagesss': 'Address change request pending for approval',
            }
            return render(request,'profile/profile.html', context)
    else:
        return redirect('home')


def cheque(request):
    if not request.user.is_authenticated:
        return request('home')
    elif request.method == 'GET':
        return render(request,'cheque.html')
    else:
        ccuser = CustomerDetails.objects.get(user=request.user)
        aa = request.POST.get('chequebook')
        if aa == '1':
            ccuser.cheque = True
            ccuser.save()
        else:
            ccuser.cheque = False
            ccuser.save()
        ad = CustomerDetails.objects.get(user=request.user)
        adr = Accounts.objects.filter(user=request.user)
        summ = 0
        for i in adr:
            summ = summ + i.balance

        context = {
                'address': ad,
                'balance': summ,
                'messages': 'Request submitted',
            }
        return render(request, 'profile/profile.html', context)