
from django.shortcuts import redirect, render
from utils.query import *

# Create your views here.

def fetch_data(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_daftar_atlet(request):
    query = """
    SELECT DISTINCT M.name, A.tgl_lahir, A.negara_asal, A.play_right, A.height, AK.world_rank, AK.world_tour_rank, A.jenis_kelamin, P.total_point
    FROM MEMBER M, ATLET A, ATLET_KUALIFIKASI AK, POINT_HISTORY P
    WHERE A.ID = P.ID_atlet
    AND A.ID = AK.ID_atlet
    AND M.ID = A.ID 
    AND total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE ID_atlet = P.ID_atlet
        ORDER BY Tahun, Bulan, Minggu_ke
        LIMIT 1
    )
    """
    cursor.execute(query)
    daftar_atlet_kualifikasi = fetch_data(cursor)

    query2 = """
    SELECT DISTINCT M.name, A.tgl_lahir, A.negara_asal, A.play_right, A.height, A.jenis_kelamin
    FROM MEMBER M, ATLET A, ATLET_NON_KUALIFIKASI ANK
    WHERE M.ID = A.ID AND A.ID = ANK.ID_atlet;
    """
    cursor.execute(query2)
    daftar_atlet_non_kualifikasi = fetch_data(cursor)

    query3 = """
    SELECT ID_Atlet_Ganda, MA.Name AS nama_atlet_1, MB.Name AS nama_atlet_2, SUM(PHA.total_point + PHB.total_point) AS total_point
    FROM MEMBER MA, MEMBER MB, ATLET_GANDA AG, POINT_HISTORY PHA, POINT_HISTORY PHB
    WHERE AG.ID_Atlet_kualifikasi=MA.ID
    AND AG.ID_Atlet_kualifikasi_2=MB.ID
    AND AG.ID_Atlet_kualifikasi=PHA.ID_Atlet
    AND AG.ID_Atlet_kualifikasi_2=PHB.ID_Atlet
    AND PHA.total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE ID_atlet=AG.ID_Atlet_kualifikasi
        ORDER BY (Tahun, Bulan, Minggu_ke) LIMIT 1
    )
    AND PHB.total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE ID_atlet=AG.ID_Atlet_kualifikasi_2
        ORDER BY (Tahun, Bulan, Minggu_ke) LIMIT 1
    )
    GROUP BY (ID_Atlet_Ganda, MA.Name , MB.Name);
    """
    cursor.execute(query3)
    daftar_atlet_ganda = fetch_data(cursor)

    context = {'daftar_atlet_kualifikasi' : daftar_atlet_kualifikasi, 'daftar_atlet_non_kualifikasi' : daftar_atlet_non_kualifikasi, 'daftar_atlet_ganda' : daftar_atlet_ganda}

    return render(request, "daftar_atlet.html", context)

