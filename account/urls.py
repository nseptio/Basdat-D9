from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    path('', show_main, name='babadu'),
    path('user', show_dashboard, name='show_dashboard'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register/umpire/', register_umpire, name='register_umpire'),
    path('register/atlet/', register_atlet, name='register_atlet'),
    path('register/pelatih/', register_pelatih, name='register_pelatih'),   
]