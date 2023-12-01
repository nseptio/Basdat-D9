from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.

# @login_required
def list_ujian_umpire(request):
    ujian_kualifikasi = query("""SELECT * FROM UJIAN_KUALIFIKASI;""")
    # print(ujian_kualifikasi)
    context = {
        "ujian_kualifikasi": ujian_kualifikasi
    }
    return render(request, "list_ujian_umpire.html", context)

# @login_required
def riwayat_ujian_umpire(request):
    riwayat_ujian_umpire = query("""SELECT NAMA, TAHUN, BATCH, TEMPAT, TANGGAL, HASIL_LULUS
                                        FROM MEMBER, ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
                                        WHERE ID=ID_ATLET;""")
    # print(riwayat_ujian_umpire)
    context = {
        "riwayat_ujian_umpire": riwayat_ujian_umpire
    }
    return render(request, "riwayat_ujian_umpire.html", context)

@csrf_exempt
def buat_ujian_umpire(request):
    if request.method == 'POST':
        tahun = int(request.POST['tahun'])
        batch = int(request.POST['batch'])
        tempat = str(request.POST['tempat'])
        tanggal = request.POST['tanggal']

        isValid = tahun and batch and tempat and tanggal
        if isValid:
            ujian = query(f"INSERT INTO UJIAN_KUALIFIKASI VALUES('{tahun}', '{batch}', '{tempat}', '{tanggal}')")
            print(ujian)
            return redirect("/umpire/ujian-kualifikasi/list")
        else:
            context = {"message": "Your input is not correct, Please check again."}
            return render(request, 'buat_ujian_umpire.html', context)
    else:
        return render(request, 'buat_ujian_umpire.html')
    
# @login_required
def daftar_ujian_atlet(request):
    ujian_kualifikasi = query("""SELECT * FROM UJIAN_KUALIFIKASI;""")
    # print(ujian_kualifikasi)
    context = {
        "ujian_kualifikasi": ujian_kualifikasi
    }
    return render(request, "daftar_ujian_atlet.html", context)

# @login_required
def soal_ujian_atlet(request):
    return render(request, "soal_ujian_atlet.html")

# @login_required
def riwayat_ujian_atlet(request):
    id = request.session['member_id']
    print(id)

    kualifikasi = query(f"""SELECT * FROM ATLET_KUALIFIKASI WHERE id_atlet = '{id}'""")
    print(kualifikasi)
    if not kualifikasi:
        kualifikasi = 'Non-Qualified'
    else:
        kualifikasi = 'Qualified'

    riwayat_ujian_atlet = query(f"""SELECT TAHUN, BATCH, TEMPAT, TANGGAL, HASIL_LULUS
                                        FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
                                        WHERE id_atlet = '{id}';""")
    print(riwayat_ujian_atlet)

    context = {
        "riwayat_ujian_atlet": riwayat_ujian_atlet
    }

    return render(request, "riwayat_ujian_atlet.html", context)