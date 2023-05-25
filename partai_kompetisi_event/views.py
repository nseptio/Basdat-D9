from django.shortcuts import render
from utils.query import *

# Create your views here.
def fetch_data(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_partai_kompetisi_event(request):
    query = """
    SELECT E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, COUNT(PPK.nomor_peserta) AS jumlah_peserta, S.Kapasitas
    FROM EVENT E, PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, STADIUM S
    WHERE E.Nama_event=PK.Nama_event
    AND E.Tahun=PK.Tahun_event
    AND PK.Nama_event=PPK.Nama_event
    AND PK.Tahun_event=PPK.Tahun_event
    AND PK.Jenis_partai=PPK.Jenis_partai
    AND E.Nama_stadium=S.Nama
    GROUP BY E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, S.Kapasitas;
    """
    cursor.execute(query)
    daftar_partai_kompetisi_event = fetch_data(cursor)

    context = {'daftar_partai_kompetisi_event' : daftar_partai_kompetisi_event}

    return render(request, "partai_kompetisi_event.html", context)

def show_partai_kompetisi_event(request):
    query = """
    SELECT E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, COUNT(PPK.nomor_peserta) AS jumlah_peserta, S.Kapasitas
    FROM EVENT E, PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, STADIUM S
    WHERE E.Nama_event=PK.Nama_event
    AND E.Tahun=PK.Tahun_event
    AND PK.Nama_event=PPK.Nama_event
    AND PK.Tahun_event=PPK.Tahun_event
    AND PK.Jenis_partai=PPK.Jenis_partai
    AND E.Nama_stadium=S.Nama
    GROUP BY E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, S.Kapasitas;
    """
    cursor.execute(query)
    daftar_partai_kompetisi_event = fetch_data(cursor)

    context = {'daftar_partai_kompetisi_event' : daftar_partai_kompetisi_event}

    return render(request, "partai_kompetisi_event.html", context)