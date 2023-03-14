from django.contrib import admin
from django.urls import path
from dashboard_lowongan_kerja_perusahaan.views import display_dashboard,display_lowongan_dibuka,display_lowongan_ditutup

urlpatterns = [
    path('dashboard-lowongan-pekerjaan/', display_dashboard, name='dashboard-lowongan-pekerjaan'),
    path('lowongan-dibuka/', display_lowongan_dibuka, name='lowongan-dibuka'),
    path('lowongan-ditutup/', display_lowongan_ditutup, name='lowongan-ditutup'),
]
