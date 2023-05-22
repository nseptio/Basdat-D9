from django.urls import path
from ungu.views import *

app_name = 'ungu'

urlpatterns = [
    path('', index, name='index'),
]