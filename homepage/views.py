from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def home(request):
    user = request.user
    if user.is_authenticated:
        if user.role_id == 1:
            return render(request, 'home.html', {'user' : user})
        elif user.role_id == 2:
            return redirect("/dashboard-lowongan-pekerjaan")
        elif user.role_id == 3 or user.role_id == 4:
            return redirect("dashboard_proposal_lowongan:dashboard")
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Pastikan username dan password yang dimasukkan benar!")
            return redirect('/login/')
            
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')