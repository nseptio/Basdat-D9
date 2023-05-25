from django.shortcuts import render
from account.forms import *
from utils.query import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import re
import uuid

# Create your views here.
def show_main(request):
    return render(request, 'main.html')

def register(request):
    return render(request, 'register.html')

def show_dashboard(request):
    if request.COOKIES.get("role"):
        email = request.COOKIES.get("email")
        if request.COOKIES.get("role") == "umpire":
            cursor.execute(
                f"SELECT * FROM UMPIRE NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'"
            )
            umpire = cursor.fetchmany()
            return dashboard_umpire(request, email, umpire)
        elif request.COOKIES.get("role") == "atlet":
            cursor.execute(
                f"SELECT * FROM ATLET NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'"
            )
            atlet = cursor.fetchmany()
            
            return dashboard_atlet(request, email, atlet)
        else:
            cursor.execute(
                f"SELECT * FROM PELATIH NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'"
            )
            pelatih = cursor.fetchmany()
            return dashboard_pelatih(request, email, pelatih)

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
                f"insert into UMPIRE (ID, Negara) values ('{uuid_umpire}', '{negara}')"
            )            

            connection.commit()

            # set cookie and redirect to dashboard
            response = HttpResponseRedirect(reverse("account:show_dashboard"))
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
        cursor.execute(f"SELECT * FROM MEMBER WHERE email = '{email}'")
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
            uuid_atlet = uuid.uuid4()
            play = True if play == "Kanan" else False
            jenis_kelamin = True if jenis_kelamin == "Laki-laki" else False
            
            cursor.execute(
                f"insert into MEMBER (ID, Name, email) values ('{uuid_atlet}', '{name}', '{email}')"
            )
            cursor.execute(
                f"""
                INSERT INTO ATLET(ID, Tgl_Lahir, Negara_Asal, Play_Right, Height, World_Rank, Jenis_Kelamin)
                VALUES ('{uuid_atlet}', '{tanggal_lahir}', '{negara}',  '{play}', '{tinggi_badan}', DEFAULT,'{jenis_kelamin}');
                """
            )
            connection.commit()

            # set cookie and redirect to dashboard
            response = HttpResponseRedirect(reverse("account:show_dashboard")) #TODO: change to dashboard
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
        form = RegisterFormPelatih(request.POST or None)
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        negara = request.POST.get("negara")
        kategori = request.POST.getlist("kategori")
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
        if not email or not negara or not nama or not kategori or not tanggal_mulai:
            form = RegisterFormPelatih(request.POST or None)
            context = {
                "form": form,
                "message": "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu",
            }
            return render(request, "register-pelatih.html", context)
        
        # check email is already registered or not
        cursor.execute(f"SELECT * FROM MEMBER WHERE email = '{email}'")
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
            uuid_pelatih = uuid.uuid4()
            cursor.execute(
                f"insert into MEMBER (ID, Name, email) values ('{uuid_pelatih}', '{name}', '{email}')"
            )
            cursor.execute(
                f"insert into PELATIH values ('{uuid_pelatih}', '{tanggal_mulai}')"
            )
            
            list_uuid_kategori = []
            for i in kategori:
                cursor.execute(f"SELECT ID FROM SPESIALISASI WHERE Spesialisasi = '{i}'")
                records = cursor.fetchmany()
                list_uuid_kategori.append(records[0][0])
                
            for i in list_uuid_kategori:
                cursor.execute(
                    f"insert into PELATIH_SPESIALISASI values ('{uuid_pelatih}', '{i}')"
                )
                
            connection.commit()

            # set cookie and redirect to dashboard
            response = HttpResponseRedirect(reverse("account:show_dashboard")) #TODO: change to dashboard
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

def dashboard_umpire(request, email, umpire):
    negara = umpire[0][1]
    nama = umpire[0][2]
    
    context = {
        "role": "umpire",
        "email": email,
        "negara": negara,
        "nama": nama,
    }
    response = render(request, "dashboard-umpire.html", context)
    response.set_cookie("role", "umpire")
    response.set_cookie("email", email)
    return response

def dashboard_atlet(request, email, atlet):
    tanggal_lahir = atlet[0][1]
    negara = atlet[0][2]
    is_play_right = atlet[0][3]
    tinggi_badan = atlet[0][4]
    world_ranking = atlet[0][5]
    is_male = atlet[0][6]
    nama = atlet[0][7]
    
    play = "Kanan" if is_play_right else "Kiri"
    gender = "Laki-Laki" if is_male else "Perempuan"
    
    context = {
        "role": "atlet",
        "email": email,
        "tanggal_lahir": tanggal_lahir,
        "negara": negara,
        "play": play,
        "tinggi_badan": tinggi_badan,
        "world_ranking": world_ranking,
        "gender": gender,
        "nama": nama,
    }
    response = render(request, "dashboard-atlet.html", context)
    response.set_cookie("role", "atlet")
    response.set_cookie("email", email)
    return response

def dashboard_pelatih(request, email, pelatih):
    tanggal_mulai = pelatih[0][1]
    nama = pelatih[0][2]
    cursor.execute(
        "SELECT name, tanggal_mulai, spesialisasi FROM MEMBER M NATURAL JOIN PELATIH P JOIN PELATIH_SPESIALISASI PS ON " +
        f"P.id = PS.id_pelatih JOIN SPESIALISASI S ON PS.id_spesialisasi = S.id WHERE M.email = '{email}';")
    pelatih_data = cursor.fetchall()
    kategori = []
    for data in pelatih_data:
        kategori.append(data[2])
    
    context = {
        "role": "pelatih",
        "email": email,
        "tanggal_mulai": tanggal_mulai,
        "nama": nama,
        "kategori": kategori,
    }
    
    response = render(request, "dashboard-pelatih.html", context)
    response.set_cookie("role", "pelatih")
    response.set_cookie("email", email)
    return response
        
def login(request):
    # if request.COOKIES.get("role"):
    #     return HttpResponseRedirect(reverse("account:register"))
    
    if request.method == "POST":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        
        cursor.execute(f"select email, name from member where email = '{email}'")
        user = cursor.fetchone()
        if(len(user) == 0):
            context = {
                'message': 'email tidak ditemukan!',
                'status': 'error',
            }
            return render(request, 'login.html', context)
        nama_database = user[1]
        email_database = user[0]

        if(email != email_database or nama != nama_database):
            context = {
                'message': 'Cek kembali email dan nama anda!',
                'status': 'error',
            }
            return render(request, 'login.html', context)
        else:
            cursor.execute(
                f"SELECT * FROM UMPIRE NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'"
            )
            umpire = cursor.fetchmany()
            if len(umpire) == 1:
                
                response = HttpResponseRedirect(reverse("account:show_dashboard"))
                response.set_cookie("role", "umpire")
                response.set_cookie("email", email)
                return response
            
            cursor.execute(
                f"SELECT * FROM PELATIH NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'"
            )
            pelatih = cursor.fetchmany()
            if len(pelatih) == 1:
                response = HttpResponseRedirect(reverse("account:show_dashboard"))
                response.set_cookie("role", "pelatih")
                response.set_cookie("email", email)
                return response
            
            cursor.execute(
                f"SELECT * FROM ATLET NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'"
            )
            atlet = cursor.fetchmany()
            if len(atlet) == 1:
                response = HttpResponseRedirect(reverse("account:show_dashboard"))
                response.set_cookie("role", "atlet")
                response.set_cookie("email", email)
                return response
            
            
    context = {}
    return render(request, "login.html", context)
                
def logout(request):
    response = HttpResponseRedirect(reverse("account:login"))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response