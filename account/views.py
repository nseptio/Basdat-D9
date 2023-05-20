from django.shortcuts import render
from account.forms import *
from utils.query import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import re
import uuid

# Create your views here.

def show_main(request):
    if request.COOKIES.get("role"):
        email = request.COOKIES.get("email")
        if request.COOKIES.get("role") == "umpire":
            return dashboard_umpire(request, email)
        elif request.COOKIES.get("role") == "atlet":
            return dashboard_atlet(request, email)
        else:
            return dashboard_pelatih(request, email)


def register(request):
    return render(request, 'register.html')

def register_umpire(request):
    if request.method == "POST" or "post" and not request.method == "GET":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        negara = request.POST.get("negara")
    
        # check email is valid or not
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        if not re.fullmatch(regex, email):
            form = RegisterFormUmpire(request.POST or None)
            context = {
                "form": form,
                "message": "Email tidak valid",
            }
            return render(request, "register-umpire.html", context)

        # if data is not complete
        if not email or not negara or not nama:
            form = RegisterFormUmpire(request.POST or None)
            context = {
                "form": form,
                "message": "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu",
            }
            return render(request, "register-umpire.html", context)
        
        # check email is already registered or not
        cursor.execute(f"SELECT * FROM MEMBER WHERE email = '{email}'")
        records = cursor.fetchmany()
        if len(records) > 0:
            form = RegisterFormUmpire(request.POST or None)
            context = {
                "form": form,
                "message": "Email sudah terdaftar",
            }
            return render(request, "register-umpire.html", context)
        
        # insert data to database
        fname = None
        lname = None
        nama = None
        # if name only contains one word
        if len(nama.split()) == 1:
            fname = nama
            lname = nama
            nama = nama
        else:
            fname = nama.split()[0]
            lname = " ".join(nama.split()[1:])
            name = fname + " " + lname

        try:
            uuid_umpire = uuid.uuid4()
            cursor.execute(
                f"insert into MEMBER (ID, Name, email) values ('{uuid_umpire}', '{name}', '{email}')"
            )
            print("aaaaa")
            
            cursor.execute(
                f"insert into UMPIRE (ID, Negara) values ('{uuid_umpire}', '{negara}')"
            )            

            connection.commit()

            # set cookie and redirect to dashboard
            response = HttpResponseRedirect(reverse("account:register"))
            response.set_cookie("role", "umpire")
            response.set_cookie("email", email)
            return response
        except Exception as err:
            connection.rollback()
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            # err slice to get only error message
            err = str(err).split("CONTEXT")[0]
            form = RegisterFormUmpire(request.POST or None)
            context = {
                "form": form,
                "message": err,
            }

            return render(request, "register-umpire.html", context)

    form = RegisterFormUmpire(request.POST or None)
    context = {"form": form}

    return render(request, "register-umpire.html", context)

def register_atlet(request):
    if request.method == "POST" or "post" and not request.method == "GET":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        negara = request.POST.get("negara")
        tanggal_lahir = request.POST.get("tanggal_lahir")
        play = request.POST.get("play")
        tinggi_badan = request.POST.get("tinggi_badan")
        jenis_kelamin = request.POST.get("jenis_kelamin")
    
        # check email is valid or not
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        if not re.fullmatch(regex, email):
            form = RegisterFormAtlet(request.POST or None)
            context = {
                "form": form,
                "message": "Email tidak valid",
            }
            return render(request, "register-umpire.html", context)

        # if data is not complete
        if (not email or
            not negara or
            not nama or
            not tanggal_lahir or
            not play or
            not tinggi_badan or
            not jenis_kelamin):
            form = RegisterFormAtlet(request.POST or None)
            context = {
                "form": form,
                "message": "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu",
            }
            return render(request, "register-umpire.html", context)
        
        # check email is already registered or not
        cursor.execute(f"SELECT * FROM ATLET WHERE email = '{email}'")
        records = cursor.fetchmany()
        if len(records) > 0:
            form = RegisterFormAtlet(request.POST or None)
            context = {
                "form": form,
                "message": "Email sudah terdaftar",
            }
            return render(request, "register-atlet.html", context)
        
        # insert data to database
        fname = None
        lname = None
        nama = None
        # if name only contains one word
        if len(nama.split()) == 1:
            fname = nama
            lname = nama
            nama = nama
        else:
            fname = nama.split()[0]
            lname = " ".join(nama.split()[1:])
            name = fname + " " + lname

        try:
            uuid_umpire = uuid.uuid4()
            jenis_kelamin = "L" if jenis_kelamin else "P"
            cursor.execute(
                f"insert into MEMBER (ID, Name, email) values ('{uuid_umpire}', '{name}', '{email}')"
            )
            cursor.execute(
                f"insert into atlet(ID, Tgl_Lahir, Negara_Asal, Play_Right, Height, World_Rank, Jenis_Kelamin)" +
                "values ('{uuid_umpire}', '{tanggal_lahir}', '{negara}',  '{play}', '{tinggi_badan}', '{jenis_kelamin})"
            )
            connection.commit()

            # set cookie and redirect to dashboard
            response = HttpResponseRedirect(reverse("account:show_main"))
            response.set_cookie("role", "atlet")
            response.set_cookie("email", email)
            return response
        except Exception as err:
            connection.rollback()
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            # err slice to get only error message
            err = str(err).split("CONTEXT")[0]
            form = RegisterFormAtlet(request.POST or None)
            context = {
                "form": form,
                "message": err,
            }

            return render(request, "register-atlet.html", context)

    form = RegisterFormAtlet(request.POST or None)
    context = {"form": form}

    return render(request, "register-atlet.html", context)

def register_pelatih(request):
    if request.method == "POST" or "post" and not request.method == "GET":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        negara = request.POST.get("negara")
        kategori = request.POST.get("kategori")
        tanggal_mulai = request.POST.get("tanggal_mulai")
    
        # check email is valid or not
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        if not re.fullmatch(regex, email):
            form = RegisterFormPelatih(request.POST or None)
            context = {
                "form": form,
                "message": "Email tidak valid",
            }
            return render(request, "register-pelatih.html", context)

        # if data is not complete
        if not email or not negara or not nama or not kategori:
            form = RegisterFormPelatih(request.POST or None)
            context = {
                "form": form,
                "message": "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu",
            }
            return render(request, "register-pelatih.html", context)
        
        # check email is already registered or not
        cursor.execute(f"SELECT * FROM UMPIRE WHERE email = '{email}'")
        records = cursor.fetchmany()
        if len(records) > 0:
            form = RegisterFormPelatih(request.POST or None)
            context = {
                "form": form,
                "message": "Email sudah terdaftar",
            }
            return render(request, "register-pelatih.html", context)
        
        # insert data to database
        fname = None
        lname = None
        nama = None
        # if name only contains one word
        if len(nama.split()) == 1:
            fname = nama
            lname = nama
            nama = nama
        else:
            fname = nama.split()[0]
            lname = " ".join(nama.split()[1:])
            name = fname + " " + lname

        try:
            uuid_umpire = uuid.uuid4()
            cursor.execute(
                f"insert into MEMBER (ID, Name, email) values ('{uuid_umpire}', '{name}', '{email}')"
            )
            cursor.execute(
                f"insert into PLEATIH values ('{uuid_umpire}', '{negara}', '{kategori}', '{tanggal_mulai}')"
            )
            connection.commit()

            # set cookie and redirect to dashboard
            response = HttpResponseRedirect(reverse("account:register"))
            response.set_cookie("role", "pelatih")
            response.set_cookie("email", email)
            return response
        except Exception as err:
            connection.rollback()
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            # err slice to get only error message
            err = str(err).split("CONTEXT")[0]
            form = RegisterFormPelatih(request.POST or None)
            context = {
                "form": form,
                "message": err,
            }

            return render(request, "register-pelatih.html", context)

    form = RegisterFormPelatih(request.POST or None)
    context = {"form": form}

    return render(request, "register-pelatih.html", context)

def dashboard_umpire(request, email):
    cursor.execute(f"SELECT * FROM MEMBER WHERE email = '{email}'")
    member_data = cursor.fetchmany()[0]
    uuid = member_data[0]
    name = member_data[1]
    
    cursor.execute(f"SELECT * FROM UMPIRE WHERE id = '{uuid}'")
    umpire_data = cursor.fetchmany()[0]
    negara = umpire_data[1]
    
    context = {
        "name": name,
        "email": email,
        "negara": negara,
    }
    
    response = render(request, "dashboard-umpire.html", context)
    response.set_cookie("role", "umpire")
    response.set_cookie("email", email)
    return response

def dashboard_atlet(request, email):
    cursor.execute(f"SELECT * FROM MEMBER WHERE email = '{email}'")
    member_data = cursor.fetchmany()[0]
    uuid = member_data[0]
    name = member_data[1]
    
    cursor.execute(f"SELECT * FROM ATLET WHERE id = '{uuid}'")
    atlet_data = cursor.fetchmany()[0]
    negara = atlet_data[1]
    
    context = {
        "name": name,
        "email": email,
        "negara": negara,
    }
    
    response = render(request, "dashboard-atlet.html", context)
    response.set_cookie("role", "atlet")
    response.set_cookie("email", email)
    return response

def dashboard_pelatih(request, email):
    cursor.execute(f"SELECT * FROM MEMBER WHERE email = '{email}'")
    member_data = cursor.fetchmany()[0]
    uuid = member_data[0]
    name = member_data[1]
    
    cursor.execute(f"SELECT * FROM PELATIH WHERE id = '{uuid}'")
    pelatih_data = cursor.fetchmany()[0]
    tanggal_mulai = pelatih_data[1]
    
    cursor.execute(f"SELECT * FROM PELATIH_SPESIALISASI WHERE id = '{uuid}'")
    
    
    context = {
        "name": name,
        "email": email,
        "tanggal_mulai": tanggal_mulai,
    }
    
    response = render(request, "dashboard-pelatih.html", context)
    response.set_cookie("role", "pelatih")
    response.set_cookie("email", email)
    return response
        
    



    

