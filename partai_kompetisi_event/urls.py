from django.urls import path
from partai_kompetisi_event.views import *

app_name = 'partai_kompetisi_event'

urlpatterns = [
    path('partai_kompetisi_event/', show_partai_kompetisi_event, name='show_partai_kompetisi_event'),
]