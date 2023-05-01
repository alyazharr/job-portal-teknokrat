from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobseeker.models import CV, Lamar, Lowongan, Users
from django.contrib import messages
from cv.forms import UserForm, CVForm

HOMEPAGE_LOGIN = 'homepage:login'
MSG_NO_AUTHORIZED = 'Anda tidak memiliki akses ke laman ini. Silakan login sebagai Admin.'


@login_required(login_url='/login/')
def profile(request):
    user = request.user
    cv = CV.objects.filter(users_id=user.id).first()
    context = {
        'cv': cv
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def resume(request, username):
    user = Users.objects.filter(username=username).first()
    if not user:
        context = {'message': 'User tidak ditemukan.'}
        return render(request, 'resume.html', context)
    cv = CV.objects.filter(users_id=user.id).first()
    context = {
        'user': user,
        'cv': cv
    }
    return render(request, 'resume.html', context)

@login_required(login_url='/login/')
def edit_resume(request):
    if request.method == 'GET':
        user = request.user
        cv = CV.objects.filter(users_id=user.id).first()
        print(user.tgl_lahir)
        user_form = UserForm(instance=user, initial={'tgl_lahir': user.tgl_lahir.strftime('%Y-%m-%d') if user.tgl_lahir else '',})
        cv_form = CVForm(instance=cv)
        context = {
            'user_form': user_form,
            'cv_form': cv_form
        }
        return render(request, 'edit_resume.html', context)
    if request.method == 'POST':
        user = request.user
        cv = CV.objects.filter(users_id=user.id).first()
        user_form = UserForm(request.POST, instance=user)
        cv_form = CVForm(request.POST, request.FILES, instance=cv)
        if user_form.is_valid() and cv_form.is_valid():
            user_form.save()
            cv_form.save()
            messages.success(request, 'CV berhasil diperbarui.')
            return redirect('cv:resume' , username=user.username)
        else:
            messages.error(request, 'CV gagal diperbarui.')
            context = {
                'user_form': user_form,
                'cv_form': cv_form
            }
            return render(request, 'edit_resume.html', context)

@login_required(login_url='/login/')
def riwayat_lamaran(request):
    user = request.user
    msg_feedback = MSG_NO_AUTHORIZED
    context = {}
    if (user.role_id == 1):
        msg_feedback = ''
        lamaran_obj = Lamar.objects.filter(users_id=user.id)
        pending_lamaran = Lamar.objects.filter(users_id=user.id, status=Lamar.StatusLamaran.PENDING)
        diterima_lamaran = Lamar.objects.filter(users_id=user.id, status=Lamar.StatusLamaran.DITERIMA)
        ditolak_lamaran = Lamar.objects.filter(users_id=user.id, status=Lamar.StatusLamaran.DITOLAK)

        if len(lamaran_obj) > 0:
            lamar_lowongan_company = [
                (
                lamar, 
                 Lowongan.objects.filter(id=lamar.lowongan_id.id).first(), 
                 Users.objects.filter(
                    id=Lowongan.objects.filter(id=lamar.lowongan_id.id).first().users_id.id)
                )
                for lamar in lamaran_obj
            ]
            context = {
                'lamaran_lowongan_company':lamar_lowongan_company,
                'msg':len(lamaran_obj),
                'total':len(lamaran_obj),
                'ditolak':len(ditolak_lamaran),
                'pending':len(pending_lamaran),
                'diterima':len(diterima_lamaran)
            }
        else:
            context['msg'] = 'Tidak ada lamaran pekerjaan.'
            context = {
                'msg':'Tidak ada lamaran pekerjaan.',
                'total':0,
                'ditolak':0,
                'pending':0,
                'diterima':0
            }
        messages.info(request, msg_feedback)
    else:
        messages.info(request, msg_feedback)
        return redirect(HOMEPAGE_LOGIN)
    return render(request, 'riwayat_lamaran.html', context)