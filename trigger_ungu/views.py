from django.shortcuts import render
from utils.query import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from trigger_ungu.forms import *

def show_partai_kompetisi(request):
    email = request.COOKIES.get('email')
    cursor.execute(
    f"""
    SELECT 
        E.nama_event,
        E.tahun,
        E.nama_stadium,
        PPK.jenis_partai,
        E.kategori_superseries,
        E.tgl_mulai,
        E.tgl_selesai 
    FROM MEMBER M
    NATURAL JOIN ATLET A
    JOIN ATLET_KUALIFIKASI AK ON A.id = AK.id_atlet
    JOIN PESERTA_KOMPETISI PK ON PK.id_atlet_kualifikasi = AK.id_atlet
    JOIN PARTAI_PESERTA_KOMPETISI PPK ON PPK.nomor_peserta = PK.nomor_peserta
    JOIN EVENT E
        ON (PPK.nama_event = E.nama_event AND PPK.tahun_event = E.tahun)
    WHERE M.email = '{email}';               
    """)
    record = cursor.fetchall()
    context = {
        "record": record
    }
    
    return render(request, 'enrolled-partai-kompetisi.html', context)

def show_enrolled_event(request):
    email = request.COOKIES.get('email')
    cursor.execute(
    f"""
    SELECT 
        E.nama_event,
        E.tahun,
        E.nama_stadium,
        E.kategori_superseries,
        E.tgl_mulai,
        E.tgl_selesai
    FROM MEMBER M
    NATURAL JOIN ATLET A
    JOIN ATLET_KUALIFIKASI AK ON A.id = AK.id_atlet
    JOIN PESERTA_KOMPETISI PK ON PK.id_atlet_kualifikasi = AK.id_atlet
    JOIN PARTAI_PESERTA_KOMPETISI PPK ON PPK.nomor_peserta = PK.nomor_peserta
    JOIN EVENT E
        ON (PPK.nama_event = E.nama_event AND PPK.tahun_event = E.tahun)
    WHERE M.email = '{email}';               
    """)
    record = cursor.fetchall()
    context = {
        "record": record
    }
    return render(request, 'enrolled-event-atlet.html', context)

def register_sponsor(request):
    if request.method == 'POST' or "post":
        email = request.COOKIES.get("email")
        form = SponsorRegistrationForm(data=request.POST, email=email)
        if form.is_valid():
            sponsor = form.cleaned_data['sponsor']
            tgl_mulai = form.cleaned_data['tanggal_mulai']
            tgl_selesai = form.cleaned_data['tanggal_selesai']
        
            if not sponsor or not tgl_mulai or not tgl_selesai:
                return render(request, 'daftar-sponsor.html', {"message": "Data tidak boleh kosong"})
        
            cursor.execute(f"""
            SELECT id
            FROM SPONSOR
            WHERE nama_brand = '{sponsor}';
            """)
            data_sponsor = cursor.fetchone()
            id_sponsor = data_sponsor[0]
            
            cursor.execute(f"SELECT * FROM ATLET NATURAL JOIN MEMBER WHERE MEMBER.email = '{email}'")
            data_atlet = cursor.fetchone()
            id_atlet = data_atlet[0]
            
            cursor.execute(f"""
            INSERT INTO ATLET_SPONSOR (ID_Atlet, ID_Sponsor, Tgl_Mulai, Tgl_Selesai)
            VALUES ('{id_atlet}', '{id_sponsor}', '{tgl_mulai}', '{tgl_selesai}');
            """)
            response = HttpResponseRedirect(reverse('trigger_ungu:show_list_sponsor'))
            return response
    
    context = {
        'form': form,
    }

    return render(request, 'daftar-sponsor.html', context)

def show_list_sponsor(request):
    email = request.COOKIES.get('email')
    cursor.execute(
    f"""
    SELECT 
        S.nama_brand,
        ASp.tgl_mulai,
        ASp.tgl_selesai
    FROM MEMBER M
    NATURAL JOIN ATLET A
    JOIN ATLET_SPONSOR ASp ON A.id = ASp.id_atlet
    JOIN SPONSOR S ON S.id = ASp.id_sponsor
    WHERE M.email = '{email}';               
    """)
    record = cursor.fetchall()
    context = {
        "record": record
    }
    return render(request, 'list-sponsor.html', context)