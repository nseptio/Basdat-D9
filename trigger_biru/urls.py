from django.urls import path
from trigger_biru.views import daftar_stadium, daftar_event, daftar_partai

app_name = 'trigger_biru'

urlpatterns = [
    path('daftar-event/', daftar_stadium, name='daftar_stadium'),
    path('daftar-event/<str:nama_stadium>/', daftar_event, name='daftar_event'),
    path('daftar-event/<str:nama_stadium>/<str:nama_event>/<int:tahun_event>/', daftar_partai, name='daftar_partai'),
]