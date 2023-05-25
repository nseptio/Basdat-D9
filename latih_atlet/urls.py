from django.urls import path
from latih_atlet.views import *

app_name = 'latih_atlet'

urlpatterns = [
    path('latih_atlet/', show_latih_atlet, name='show_latih_atlet'),
    path('list_atlet_dilatih/', show_list_atlet_dilatih, name='show_list_atlet_dilatih'),
]