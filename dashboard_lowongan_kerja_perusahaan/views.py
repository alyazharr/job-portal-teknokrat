from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from jobseeker.models import Lowongan,Lamar
from django.contrib.auth.decorators import login_required
from datetime import date


global HOMEPAGE_LOGIN
HOMEPAGE_LOGIN = 'homepage:login'

@login_required(login_url=HOMEPAGE_LOGIN)
def display_dashboard(request):
    user = request.user
    if (user.role_id == 2):
        data = Lowongan.objects.filter(users_id = user.id)
        total_lowongan = data.count()
        total_dibuka = Lowongan.objects.filter(users_id = user.id, status='Buka').count()
        total_ditutup = Lowongan.objects.filter(users_id = user.id, status='Tutup').count()
    else:
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, 'dashboard_lowongan_kerja_perusahaan.html', {'lowongan_pekerjaan': data,'total_lowongan':total_lowongan,'total_dibuka':total_dibuka,'total_ditutup':total_ditutup})

@login_required(login_url=HOMEPAGE_LOGIN)
def display_lowongan_dibuka(request):
    user = request.user
    if (user.role_id == 2):
        data = Lowongan.objects.filter(users_id = user.id, status='Buka')
    else: 
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, 'lowongan_dibuka.html', {'lowongan_dibuka': data})

@login_required
def display_lowongan_ditutup(request):
    user = request.user
    if (user.role_id == 2):
        data = Lowongan.objects.filter(users_id = user.id, status='Tutup')
    else:
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, 'lowongan_ditutup.html', {'lowongan_ditutup': data})

@login_required(login_url=HOMEPAGE_LOGIN)
def ubah_status(request,id):
    user = request.user
    if (user.role_id == 2):
        lowongan = Lowongan.objects.get(users_id = user.id, id=id)
    else:
        return redirect(HOMEPAGE_LOGIN) 
    if lowongan.status =='Buka':
        lowongan.status = "Tutup"
    lowongan.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def pelamar_lowongan(request, id):
    user = request.user
    if user.role_id == 2:
        lowongan = Lowongan.objects.get(users_id=user.id, id=id)
        data = Lamar.objects.filter(lowongan_id=lowongan)
        total_pelamar = data.count()
        pelamar_diterima = Lamar.objects.filter(lowongan_id=lowongan, status='Diterima').count()
        pelamar_ditolak = Lamar.objects.filter(lowongan_id=lowongan, status='Ditolak').count()
        
        sort_by_ipk = request.GET.get('sort_by_ipk')
        sort_by_date = request.GET.get('sort_by_date')
        if sort_by_ipk:
            data = data.order_by('-users_id__ipk')  # Sort by IPK from highest to lowest
        if sort_by_date:
            data = data.order_by('-created_at')

    else:
        return redirect(HOMEPAGE_LOGIN) 

    context = {
        'pelamar': data,
        'lowongan': lowongan,
        'total_pelamar': total_pelamar,
        'pelamar_diterima': pelamar_diterima,
        'pelamar_ditolak': pelamar_ditolak,
    }
    return render(request, 'dashboard_pelamar.html', context)

login_required(login_url=HOMEPAGE_LOGIN)
def terima_pelamar(request,id):
    user = request.user
    if (user.role_id == 2):
        lamaran = Lamar.objects.get(id=id)
        lamaran.status ="Diterima"
        lamaran.save()
    else:
        return redirect(HOMEPAGE_LOGIN) 
    return redirect(request.META.get('HTTP_REFERER', '/'))

login_required(login_url=HOMEPAGE_LOGIN)
def tolak_pelamar(request,id):
    user = request.user
    if (user.role_id == 2):
        lamaran = Lamar.objects.get(id=id)
        lamaran.status ="Ditolak"
        lamaran.save()
    else:
        return redirect(HOMEPAGE_LOGIN) 
    return redirect(request.META.get('HTTP_REFERER', '/'))
    

