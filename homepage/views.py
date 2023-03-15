from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

def home(request):
    user = request.user
    return render(request, 'home.html', {'user' : user})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login/')
            
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')