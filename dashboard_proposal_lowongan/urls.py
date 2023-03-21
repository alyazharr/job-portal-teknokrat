from django.urls import path
from .views import dashboard, detail, dashboard_riwayat, dashboard_terverifikasi
app_name = "dashboard_proposal_lowongan"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("detail/<int:id>", detail, name="detail"),
    path("verifikasi",dashboard_terverifikasi,name='terverifikasi'),
    path("riwayat", dashboard_riwayat, name='riwayat')
]
