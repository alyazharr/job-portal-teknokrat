from django.urls import path
from cv.views import profile, riwayat_lamaran, resume, edit_resume

app_name = 'cv'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('riwayat-lamaran/', riwayat_lamaran, name='riwayat-lamaran'),
    path('resume/<str:username>/', resume, name='resume'),
    path('resume/edit', edit_resume, name='edit-resume')
]