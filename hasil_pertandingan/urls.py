from django.urls import path
from hasil_pertandingan.views import *

app_name = 'hasil_pertandingan'

urlpatterns = [
    path('hasil_pertandingan/', show_hasil_pertandingan, name='show_hasil_pertandingan'),
]