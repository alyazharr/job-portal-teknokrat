"""jobseeker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cv.urls")),
    path("", include('homepage.urls')),
    path("", include('dashboard_lowongan_kerja_perusahaan.urls')),
    path("buka_lowongan/", views.BukaLowonganFormView.as_view(),name='buka_lowongan'),
    path("edit-lowongan/<int:pk>", views.EditLowonganFormView.as_view(),name='edit-lowongan'),
    path("list_lowongan/",views.ListLowonganView.as_view(),name='list_lowongan'),
    path("detail_lowongan/<int:pk>/", views.DetailLowonganView.as_view(),name='detail_lowongan'),
    path("dashboard-proposal-lowongan/", include("dashboard_proposal_lowongan.urls")),
    path("notification/", include("notification.urls"))
]

