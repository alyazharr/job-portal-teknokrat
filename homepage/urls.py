from django.urls import path
from homepage.views import home, login_user, logout_user

app_name = 'homepage'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]