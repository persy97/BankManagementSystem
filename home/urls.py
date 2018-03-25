from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('send/', views.send, name='send'),
    path('history/', views.history, name='history'),
    path('logout/', views.logoutt, name='logoutt'),
    path('changepassword/', views.changepass, name='changepass'),
    path('changeaddress/', views.change, name='changeaddr'),
    path('cheque/', views.cheque, name='cheque'),
]