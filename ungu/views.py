from django.shortcuts import render
from account.forms import *
from utils.query import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import re
import uuid

# Create your views here.

def index(request):
    return render(request, 'list-sponsor.html')