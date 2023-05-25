from django.urls import path
from ujian_kualifikasi.views import *
app_name = 'ujian_kualifikasi'

urlpatterns = [
    path('', list_ujian_umpire, name='list_ujian_umpire'),
    path('ujian-kualifikasi/riwayat', riwayat_ujian_umpire, name='riwayat_ujian_umpire'),
    path('ujian-kualifikasi/buat', buat_ujian_umpire, name='buat_ujian_umpire'),
    path('ujian-kualifikasi/daftar', daftar_ujian_atlet, name='pilih_ujian_atlet'),
    path('ujian-kualifikasi/soal', soal_ujian_atlet, name='soal_ujian_atlet'),
    path('ujian-kualifikasi/riwayata', riwayat_ujian_atlet, name='riwayat_ujian_atlet'),
]