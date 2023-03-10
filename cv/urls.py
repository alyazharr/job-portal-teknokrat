from django.urls import path
from cv.views import profile

app_name = 'cv'

urlpatterns = [
    path('profile/', profile, name='profile'),
]