from django.shortcuts import render

# Create your views here.

def show_hasil_pertandingan(request):
    return render(request, "hasil_pertandingan.html")
