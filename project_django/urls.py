"""project_django URL Configuration

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
from daftar_atlet.views import show_daftar_atlet
from partai_kompetisi_event.views import show_partai_kompetisi_event
from hasil_pertandingan.views import show_hasil_pertandingan
from latih_atlet.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('pink_hasil_pertandingan/', include('hasil_pertandingan.urls')),
    path('pink_latih_atlet/', include('latih_atlet.urls')),
    path('pink_daftar_atlet/', include('daftar_atlet.urls')),
    path('pink_partai_kompetisi_event/', include('partai_kompetisi_event.urls')),
    path('ungu/', include('trigger_ungu.urls')),
    path('biru/', include('trigger_biru.urls')),
]