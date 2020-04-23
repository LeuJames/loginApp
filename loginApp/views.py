from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    request.session['name'] = request.POST['f_name']
    password = request.POST['pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    User.objects.create(
        f_name=request.POST['f_name'],
        l_name=request.POST['l_name'],
        email=request.POST['email'],
        password=pw_hash,
        dob=request.POST['dob']
        )
    return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
            return redirect('/')
    request.session['name']=User.objects.get(email=request.POST['email']).f_name
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect ('/')

def success(request):
    print(request.session)
    if 'name' in request.session:
        return render(request, 'userInfo.html')
    return redirect ('/')
