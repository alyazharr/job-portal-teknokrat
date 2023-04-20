from django.urls import path
from cv.views import profile, riwayat_lamaran

app_name = 'cv'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('riwayat-lamaran/', riwayat_lamaran, name='riwayat-lamaran'),
]