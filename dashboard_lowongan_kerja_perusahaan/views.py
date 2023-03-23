from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from jobseeker.models import Lowongan
from django.contrib.auth.decorators import login_required


global HOMEPAGE_LOGIN
HOMEPAGE_LOGIN = 'homepage:login'

@login_required(login_url=HOMEPAGE_LOGIN)
def display_dashboard(request):
    user = request.user
    if (user.role_id == 2):
        data = Lowongan.objects.all()
        total_lowongan = data.count()
        total_dibuka = Lowongan.objects.filter(status='Buka').count()
        total_ditutup = Lowongan.objects.filter(status='Tutup').count()
    else:
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, 'dashboard_lowongan_kerja_perusahaan.html', {'lowongan_pekerjaan': data,'total_lowongan':total_lowongan,'total_dibuka':total_dibuka,'total_ditutup':total_ditutup})

@login_required(login_url=HOMEPAGE_LOGIN)
def display_lowongan_dibuka(request):
    user = request.user
    if (user.role_id == 2):
        data = Lowongan.objects.filter(status='Buka')
    else: 
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, 'lowongan_dibuka.html', {'lowongan_dibuka': data})

@login_required
def display_lowongan_ditutup(request):
    user = request.user
    if (user.role_id == 2):
        data = Lowongan.objects.filter(status='Tutup')
    else:
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, 'lowongan_ditutup.html', {'lowongan_ditutup': data})

@login_required(login_url=HOMEPAGE_LOGIN)
def ubah_status(request,id):
    user = request.user
    if (user.role_id == 2):
        lowongan = Lowongan.objects.get(id=id)
    else:
        return redirect(HOMEPAGE_LOGIN) 
    if lowongan.status =='Buka':
        lowongan.status = "Tutup"
    else:
         lowongan.status = "Buka"
    lowongan.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

    

