from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from jobseeker.backend import CustomBackend

# Create your views here.
def home(request):
    user = request.user
    return render(request, 'home.html', {'user' : user})

def login_user(request):
    custom_backend = CustomBackend()
    if request.method == 'POST':
        user = custom_backend.authenticate(request)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login/')
            
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')