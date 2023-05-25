from django.urls import path
from daftar_atlet.views import *

app_name = 'daftar_atlet'

urlpatterns = [
    path('daftar_atlet/', show_daftar_atlet, name='show_daftar_atlet'),
]