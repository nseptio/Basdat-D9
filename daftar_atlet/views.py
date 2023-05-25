
from django.shortcuts import redirect, render
from utils.query import *

# Create your views here.

def fetch_data(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_daftar_atlet(request):
    query = """
    SELECT DISTINCT M.name, A.tgl_lahir, A.negara_asal, A.play_right, A.height, AK.world_rank, AK.world_tour_rank, A.jenis_kelamin, P.total_point
    FROM MEMBER M
    JOIN ATLET A ON M.ID = A.ID
    JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_atlet
    JOIN POINT_HISTORY P ON A.ID = P.ID_atlet
    WHERE P.total_point = (
        SELECT total_point
        FROM POINT_HISTORY
        WHERE ID_atlet = P.ID_atlet
        ORDER BY Tahun, Bulan, Minggu_ke
        LIMIT 1
    );
    """
    cursor.execute(query)
    daftar_atlet_kualifikasi = fetch_data(cursor)

    query2 = """
    SELECT DISTINCT M.name, A.tgl_lahir, A.negara_asal, A.play_right, A.height, A.jenis_kelamin
    FROM MEMBER M, ATLET A, ATLET_NON_KUALIFIKASI ANK
    WHERE M.ID = A.ID 
    AND A.ID = ANK.ID_atlet;
    """
    cursor.execute(query2)
    daftar_atlet_non_kualifikasi = fetch_data(cursor)

    query3 = """
    SELECT AG.ID_Atlet_Ganda, M1.Name AS nama1, M2.Name AS nama2, SUM(PH1.total_point + PH2.total_point) AS total_point
    FROM ATLET_GANDA AG
    JOIN MEMBER M1 ON AG.ID_Atlet_Kualifikasi = M1.ID
    JOIN MEMBER M2 ON AG.ID_Atlet_Kualifikasi_2 = M2.ID
    JOIN POINT_HISTORY PH1 ON AG.ID_Atlet_Kualifikasi = PH1.ID_Atlet
    JOIN POINT_HISTORY PH2 ON AG.ID_Atlet_Kualifikasi_2 = PH2.ID_Atlet
    WHERE (PH1.total_point, AG.ID_Atlet_Kualifikasi) IN (
        SELECT total_point, ID_atlet
        FROM POINT_HISTORY
        WHERE ID_atlet = AG.ID_Atlet_Kualifikasi
        ORDER BY Tahun, Bulan, Minggu_ke
        LIMIT 1
    )
    AND (PH2.total_point, AG.ID_Atlet_Kualifikasi_2) IN (
        SELECT total_point, ID_atlet
        FROM POINT_HISTORY
        WHERE ID_atlet = AG.ID_Atlet_Kualifikasi_2
        ORDER BY Tahun, Bulan, Minggu_ke
        LIMIT 1
    )
    GROUP BY AG.ID_Atlet_Ganda, M1.Name, M2.Name;
    """
    cursor.execute(query3)
    daftar_atlet_ganda = fetch_data(cursor)

    context = {'daftar_atlet_kualifikasi' : daftar_atlet_kualifikasi, 'daftar_atlet_non_kualifikasi' : daftar_atlet_non_kualifikasi, 'daftar_atlet_ganda' : daftar_atlet_ganda}

    return render(request, "daftar_atlet.html", context)

