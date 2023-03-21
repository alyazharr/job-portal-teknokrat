from django.shortcuts import render, redirect
from jobseeker.models import Users, Lowongan
from django.contrib.auth.decorators import login_required
from django.contrib import messages

global HOMEPAGE_LOGIN
HOMEPAGE_LOGIN = 'homepage:login'

global MSG_NO_LOGIN
MSG_NO_LOGIN = 'Anda tidak memiliki akses ke laman ini. Silakan login sebagai Admin.'

@login_required(login_url=HOMEPAGE_LOGIN)
def dashboard(request):
    user = request.user
    msg_feedback = MSG_NO_LOGIN
    context = {}
    if (user.role_id == 3) or (user.role_id == 4):
        msg_feedback =''
        lowongan_obj = Lowongan.objects.filter(status=Lowongan.StatusLowongan.UNVERIFIED)
        verif = Lowongan.objects.filter(status=Lowongan.StatusLowongan.VERIFIED)
        total_obj = Lowongan.objects.all()
        tolak = Lowongan.objects.filter(status=Lowongan.StatusLowongan.REJECTED)
        if len(lowongan_obj) != 0:
            lowongan_with_companies = [
                (lowongan, Users.objects.filter(id=lowongan.users_id.id)) 
                for lowongan in lowongan_obj
            ]
            context = {
                'lowongan_with_companies': lowongan_with_companies,
                'msg':len(lowongan_obj),
                'total':len(total_obj),
                'terverifikasi':len(verif),
                'unverified':len(lowongan_obj),
                'tolak':len(tolak),
            }
        else:
            context = {
                'msg': "Tidak Ada Request Proposal Lowongan",
                'total':len(total_obj),
                'terverifikasi':len(verif),
                'unverified':len(lowongan_obj),
                'tolak':len(tolak),
            }
    else:
        messages.info(request, msg_feedback)
        return redirect(HOMEPAGE_LOGIN)
    return render(request, "dashboard_proposal.html", context)

@login_required(login_url=HOMEPAGE_LOGIN)
def dashboard_terverifikasi(request):
    user = request.user
    msg_feedback = MSG_NO_LOGIN
    context = {}
    if (user.role_id == 3) or (user.role_id == 4):
        msg_feedback =''
        lowongan_obj = Lowongan.objects.filter(status=Lowongan.StatusLowongan.VERIFIED)
        unverif = Lowongan.objects.filter(status=Lowongan.StatusLowongan.UNVERIFIED)
        total_obj = Lowongan.objects.all()
        tolak = Lowongan.objects.filter(status=Lowongan.StatusLowongan.REJECTED)
        if len(lowongan_obj) != 0:
            lowongan_with_companies = [
                (lowongan, Users.objects.filter(id=lowongan.users_id.id)) 
                for lowongan in lowongan_obj
            ]
            context = {
                'lowongan_with_companies': lowongan_with_companies,
                'msg':len(lowongan_obj),
                'total':len(total_obj),
                'terverifikasi':len(lowongan_obj),
                'unverified':len(unverif),
                'tolak':len(tolak)
            }
        else:
            context = {
                'msg': "Tidak Ada Proposal Lowongan Yang Terverifikasi",
                'total':len(total_obj),
                'terverifikasi':len(lowongan_obj),
                'unverified':len(unverif),
                'tolak':len(tolak)
            }
    else:
        messages.info(request, msg_feedback)
        return redirect(HOMEPAGE_LOGIN)
    return render(request, "terverifikasi.html", context)

@login_required(login_url=HOMEPAGE_LOGIN)
def dashboard_riwayat(request):
    user = request.user
    msg_feedback = MSG_NO_LOGIN
    context = {}
    if (user.role_id == 3) or (user.role_id == 4):
        msg_feedback =''
        lowongan_obj = Lowongan.objects.all()
        verif = Lowongan.objects.filter(status=Lowongan.StatusLowongan.VERIFIED)
        unverif = Lowongan.objects.filter(status=Lowongan.StatusLowongan.UNVERIFIED)
        tolak = Lowongan.objects.filter(status=Lowongan.StatusLowongan.REJECTED)
        if len(lowongan_obj) != 0:
            lowongan_with_companies = [
                (lowongan, Users.objects.filter(id=lowongan.users_id.id)) 
                for lowongan in lowongan_obj
            ]
            context = {
                'lowongan_with_companies': lowongan_with_companies,
                'msg':len(lowongan_obj),
                'total':len(lowongan_obj),
                'terverifikasi':len(verif),
                'unverified':len(unverif),
                'tolak':len(tolak),
            }
        else:
            context = {
                'msg': "Tidak Ada Riwayat Proposal Lowongan",
                'total':len(lowongan_obj),
                'terverifikasi':len(verif),
                'unverified':len(unverif),
                'tolak':len(tolak),
            }
    else:
        messages.info(request, msg_feedback)
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, "riwayat.html", context)

@login_required(login_url=HOMEPAGE_LOGIN) 
def detail(request, id):
    user = request.user
    msg_feedback = MSG_NO_LOGIN
    context = {}
    if (user.role_id == 3) or (user.role_id == 4):
        msg_feedback =''
        if Lowongan.objects.filter(id=id).exists():
            lowongan = Lowongan.objects.get(id=id)
            company = Users.objects.get(id=lowongan.users_id.id)
            context = {
                'lowongan': lowongan,
                'company':company,
                'msg':'Tersedia'
                }
    else:
        messages.info(request, msg_feedback)
        return redirect(HOMEPAGE_LOGIN) 
    return render(request, "detail_page.html", context)
