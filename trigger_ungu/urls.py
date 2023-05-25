from django.urls import path
from trigger_ungu.views import *

app_name = 'trigger_ungu'

urlpatterns = [
    path('enrolled-event/', show_enrolled_event, name='show_enrolled_event'),
    path('enrolled-partai-kompetisi/', show_partai_kompetisi, name='show_partai_kompetisi'),
    path('daftar-sponsor/', register_sponsor, name='register_sponsor'),
    path('list-sponsor/', show_list_sponsor, name='show_list_sponsor')
]