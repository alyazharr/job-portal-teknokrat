from django.contrib import admin
from django.urls import path
import dashboard_lowongan_kerja_perusahaan
from dashboard_lowongan_kerja_perusahaan.views import display_dashboard,display_lowongan_dibuka,display_lowongan_ditutup,ubah_status,pelamar_lowongan,terima_pelamar,tolak_pelamar,detail_page

urlpatterns = [
    path('dashboard-lowongan-pekerjaan/', display_dashboard, name='dashboard-lowongan-pekerjaan'),
    path('lowongan-dibuka/', display_lowongan_dibuka, name='lowongan-dibuka'),
    path('lowongan-ditutup/', display_lowongan_ditutup, name='lowongan-ditutup'),
    path('ubah_status/<int:id>/', ubah_status, name='ubah_status'),
    path('terima_pelamar/<int:id>/', terima_pelamar, name='terima_pelamar'),
    path('tolak_pelamar/<int:id>/', tolak_pelamar, name='tolak_pelamar'),
    path('pelamar_lowongan/<int:id>/', pelamar_lowongan, name='pelamar_lowongan'),
    path("detail_page/<int:id>", detail_page, name="detail_page"),
]
