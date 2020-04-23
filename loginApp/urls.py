from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('success', views.success),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]