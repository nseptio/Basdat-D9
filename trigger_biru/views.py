from django.shortcuts import redirect, render
from django.contrib import messages
import psycopg2
import locale
import uuid
locale.setlocale(locale.LC_ALL, '')

# Create your views here.

def daftar_stadium(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="asbag2006"
    )
    cursor = db_connection.cursor()
    
    cursor.execute("set search_path to babadu")
    cursor.execute("select * from STADIUM")
    context['stadium'] = cursor.fetchall()
    db_connection.close()
    return render(request, 'daftar_stadium.html', context=context)

def daftar_event(request, nama_stadium):
    db_connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="asbag2006"
    )
    cursor = db_connection.cursor()
    cursor.execute("set search_path to babadu")
    event_list = get_event_in_stadium(nama_stadium, cursor)
    print(event_list)
    context = {"daftar_event": event_list,
               "nama_stadium": nama_stadium}
    db_connection.close()
    return render(request, 'daftar_event.html', context=context)

def daftar_partai(request, nama_stadium, nama_event, tahun_event):
    # TODO: Nanti ganti id-nya make id orang yang login
    athlete_id = '9eb3ec02-b6c5-43fc-b142-7c2e2732d9bc'
    db_connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="asbag2006"
    )
    cursor = db_connection.cursor()
    cursor.execute("set search_path to babadu")
    
    if (request.method == 'POST'):
        if ('Ganda' in request.POST['jenis-partai']):
            try:
                rank_atlet = get_athlete_rank(athlete_id, cursor)
                
                email_pasangan = request.POST['partner']
                jenis_partai = request.POST['jenis-partai']
                reverse_map_partai = {
                    'Ganda Wanita' : 'WD',
                    'Ganda Putra' : 'MD',
                    'Ganda Campuran' : 'XD',
                    'Tunggal Wanita' : 'WS',
                    'Tunggal Putra' : 'MS',
                }
                
                jenis_partai = reverse_map_partai.get(jenis_partai)
                                
                cursor.execute("select id from member where email = %s", (email_pasangan))
                id_pasangan = cursor.fetchone()[0]
                
                id_atlet_ganda = get_id_atlet_ganda(athlete_id, cursor, id_pasangan)
                if (id_atlet_ganda is None):
                    id_atlet_ganda = str(uuid.uuid4())
                    create_atlet_ganda(athlete_id, cursor, id_pasangan, id_atlet_ganda)
                else:
                    id_atlet_ganda = id_atlet_ganda[0]
                
                nomor_peserta = get_nomor_peserta_ganda(cursor, id_atlet_ganda)
                
                if (nomor_peserta is None):
                    nomor_peserta = create_peserta_kompetisi(cursor, rank_atlet, id_atlet_ganda=id_atlet_ganda)
                    
                else:
                    nomor_peserta = nomor_peserta[0]
                
                insert_peserta_kompetisi(nama_event, tahun_event, cursor, jenis_partai, nomor_peserta)
                db_connection.commit()
                db_connection.close()
                
                # TODO: ATUR REDIRECT
                return redirect(request.get_full_path())
                
            except Exception as e:
                # messages.error(request, "Gagal mendaftar, mohon periksa input anda dan coba lagi")
                messages.error(request, e)
                db_connection.rollback()
                db_connection.close()
                
                # TODO: Atur Redirect
                return redirect(request.get_full_path())
        else:
            try:
                rank_atlet = get_athlete_rank(athlete_id, cursor)
                jenis_partai = request.POST['jenis-partai']
                reverse_map_partai = {
                    'Ganda Wanita' : 'WD',
                    'Ganda Putra' : 'MD',
                    'Ganda Campuran' : 'XD',
                    'Tunggal Wanita' : 'WS',
                    'Tunggal Putra' : 'MS',
                }
                
                jenis_partai = reverse_map_partai.get(jenis_partai)
                
                nomor_peserta = get_nomor_peserta_tunggal(athlete_id, cursor)
                
                if (nomor_peserta is None):
                    nomor_peserta = create_peserta_kompetisi(cursor, rank_atlet, id_atlet_kualifikasi=athlete_id)
                    
                else:
                    nomor_peserta = nomor_peserta[0]
                
                insert_peserta_kompetisi(nama_event, tahun_event, cursor, jenis_partai, nomor_peserta)
                db_connection.commit()
                db_connection.close()
                return redirect(request.get_full_path())
                
            except Exception as e:
                messages.error(request, "Gagal mendaftar, mohon periksa input anda dan coba lagi")
                messages.error(request, e)
                db_connection.rollback()
                db_connection.close()
                return redirect(request.get_full_path())
    
    data_atlet = get_athlete_data(cursor, athlete_id)
    
    data_partai = get_data_partai(nama_event, tahun_event, athlete_id, cursor)
    
    available_atlet_ganda = get_available_atlet_ganda(cursor, nama_event, tahun_event, athlete_id)
    
    data_stadium = get_stadium(nama_stadium, cursor)
    
    data_event = get_event(nama_event, tahun_event, cursor)
    
    context = {"data_event": data_event,
               "data_stadium": data_stadium,
               "available_atlet_ganda": available_atlet_ganda,
               "data_partai": data_partai,
               "data_atlet": data_atlet,}
    db_connection.close()
    return render(request, 'daftar_partai.html', context=context)

def insert_peserta_kompetisi(nama_event, tahun_event, cursor, jenis_partai, nomor_peserta):
    query_insert_partai_peserta_kompetisi = """
                INSERT INTO partai_peserta_kompetisi (nomor_peserta, jenis_partai, nama_event, tahun_event)
                VALUES (%s, %s, %s, %s)
                """
    cursor.execute(query_insert_partai_peserta_kompetisi, (nomor_peserta, jenis_partai, nama_event, tahun_event))

def get_nomor_peserta_tunggal(athlete_id, cursor):
    query_get_nomor_peserta = """
                    SELECT nomor_peserta
                    FROM peserta_kompetisi
                    WHERE id_atlet_kualifikasi = %s
                """
    cursor.execute(query_get_nomor_peserta, (athlete_id,))
    nomor_peserta = cursor.fetchone()
    return nomor_peserta

def create_peserta_kompetisi(cursor, rank_atlet, id_atlet_ganda = None, id_atlet_kualifikasi = None):
    query_get_highest_nomor_peserta = """
                    SELECT MAX(nomor_peserta)
                    FROM peserta_kompetisi
                    """
    cursor.execute(query_get_highest_nomor_peserta)
    nomor_peserta = cursor.fetchone()[0] + 1
                    
    query_insert_peserta_kompetisi = """
                        INSERT INTO peserta_kompetisi (nomor_peserta, id_atlet_kualifikasi, id_atlet_ganda, world_rank, world_tour_rank)
                        VALUES (%s, %s, %s, %s, %s)
                    """                    
    cursor.execute(query_insert_peserta_kompetisi, (nomor_peserta, id_atlet_kualifikasi, id_atlet_ganda, rank_atlet[0], rank_atlet[1]))
    return nomor_peserta

def get_nomor_peserta_ganda(cursor, id_atlet_ganda):
    query_get_nomor_peserta = """
                SELECT nomor_peserta
                FROM peserta_kompetisi
                WHERE id_atlet_ganda = %s
                """
    cursor.execute(query_get_nomor_peserta, (id_atlet_ganda))
    nomor_peserta = cursor.fetchone()
    return nomor_peserta

def create_atlet_ganda(athlete_id, cursor, id_pasangan, id_atlet_ganda):
    query_insert_atlet_ganda = """
                    INSERT INTO ATLET_GANDA (id_atlet_ganda, id_atlet_kualifikasi, id_atlet_kualifikasi_2)
                    VALUES (%s, %s, %s)
                    """
    cursor.execute(query_insert_atlet_ganda, (id_atlet_ganda, athlete_id, id_pasangan))

def get_id_atlet_ganda(athlete_id, cursor, id_pasangan):
    query_check_pair_exist = """
                SELECT AG1.id_atlet_ganda
                FROM ATLET_GANDA AG1
                WHERE (AG1.id_atlet_kualifikasi = %s AND  AG1.id_atlet_kualifikasi_2 = %s)
                OR (AG1.id_atlet_kualifikasi = %s AND  AG1.id_atlet_kualifikasi_2 = %s)
                """
    cursor.execute(query_check_pair_exist, (athlete_id, id_pasangan, id_pasangan, athlete_id))
    id_atlet_ganda = cursor.fetchone()
    return id_atlet_ganda

def get_athlete_rank(athlete_id, cursor):
    query_get_athlete_rank = """
                    select * from ATLET_KUALIFIKASI AK
                    where AK.ID_ATLET = %s
                    """
    cursor.execute(query_get_athlete_rank, (athlete_id,))
    rank_atlet = cursor.fetchone()[1:]
    return rank_atlet

def get_athlete_data(cursor, athlete_id):
    query_get_athlete_data = """
    SELECT M.name, A.Jenis_Kelamin
    FROM MEMBER M, ATLET A
    WHERE M.ID = A.ID
    AND M.ID = %s
    """
    cursor.execute(query_get_athlete_data, (athlete_id,))
    data_atlet = cursor.fetchone()
    return data_atlet

def get_data_partai(nama_event, tahun_event, id_atlet, cursor):
    query_get_partai = """
    select P.jenis_partai, count(*) 
    FROM partai_kompetisi P, EVENT E, PARTAI_PESERTA_KOMPETISI PPK 
    WHERE P.nama_event = E.nama_event
    AND P.tahun_event = E.tahun
    AND PPK.jenis_partai = P.jenis_partai
    AND PPK.nama_event = P.nama_event
    AND PPK.tahun_event = P.tahun_event
    AND P.nama_event = %s
    AND P.tahun_event = %s
    GROUP BY P.jenis_partai, P.nama_event, P.tahun_event;
    """
    
    query_status_pendaftaran_atlet = """
    SELECT EXISTS (
        (
            SELECT PK.id_atlet_kualifikasi
            FROM PARTAI_PESERTA_KOMPETISI PPK, PESERTA_KOMPETISI PK
            WHERE PPK.Nomor_Peserta = PK.Nomor_Peserta
            AND PPK.jenis_partai = %s
            AND PPK.nama_event = %s
            AND PPK.tahun_event = %s
            AND PK.ID_Atlet_Kualifikasi = %s
        )
        UNION
        (
            SELECT AG.ID_ATLET_KUALIFIKASI
            FROM PARTAI_PESERTA_KOMPETISI PPK, PESERTA_KOMPETISI PK, ATLET_GANDA AG
            WHERE PPK.Nomor_Peserta = PK.Nomor_Peserta
            AND AG.ID_Atlet_Ganda = PK.ID_Atlet_Ganda
            AND PPK.jenis_partai = %s
            AND PPK.nama_event = %s
            AND PPK.tahun_event = %s
            AND AG.ID_Atlet_Kualifikasi = %s
        )
        UNION
        (
            SELECT AG.ID_ATLET_KUALIFIKASI_2
            FROM PARTAI_PESERTA_KOMPETISI PPK, PESERTA_KOMPETISI PK, ATLET_GANDA AG
            WHERE PPK.Nomor_Peserta = PK.Nomor_Peserta
            AND AG.ID_Atlet_Ganda = PK.ID_Atlet_Ganda
            AND PPK.jenis_partai = %s
            AND PPK.nama_event = %s
            AND PPK.tahun_event = %s
            AND AG.ID_Atlet_Kualifikasi_2 = %s
        )
    ) AS Exist;
    """
    
    cursor.execute(query_get_partai, (nama_event, tahun_event))
    data_partai = cursor.fetchall()
    map_partai = {
        'WD' : 'Ganda Wanita',
        'MD' : 'Ganda Putra',
        'XD' : 'Ganda Campuran',
        'WS' : 'Tunggal Wanita',
        'MS' : 'Tunggal Putra',
    }
    
    for i in range(len(data_partai)):
        cursor.execute(query_status_pendaftaran_atlet, (data_partai[i][0], nama_event, tahun_event, id_atlet,
                                                        data_partai[i][0], nama_event, tahun_event, id_atlet,
                                                        data_partai[i][0], nama_event, tahun_event, id_atlet))
        
        status_daftar_user = cursor.fetchone()[0]
        jenis_partai = map_partai.get(data_partai[i][0])
        jumlah_orang_di_partai = data_partai[i][1]
        
        data_partai[i] = ((jenis_partai, jumlah_orang_di_partai, status_daftar_user))
    
    return data_partai

def get_available_atlet_ganda(cursor, nama_event, tahun_event, athlete_id):
    query_get_available_atlet_ganda = """
    SELECT M.NAME, A.Jenis_Kelamin, M.email
    FROM MEMBER M, ATLET A, ATLET_KUALIFIKASI AK
    WHERE M.ID = A.ID
    AND A.id = AK.id_atlet
    AND A.id <> %s
    AND A.id NOT IN (
        (SELECT AG.id_atlet_kualifikasi
        FROM PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, PESERTA_KOMPETISI PSK, ATLET_GANDA AG
        WHERE PPK.jenis_partai = PK.jenis_partai
        AND PPK.nama_event = PK.nama_event
        AND PPK.tahun_event = PK.tahun_event
        AND PPK.Nomor_Peserta = PSK.Nomor_Peserta
        AND PSK.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
        AND PPK.nama_event = %s
        AND PPK.tahun_event = %s)
        UNION
        (SELECT AG.id_atlet_kualifikasi
        FROM PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, PESERTA_KOMPETISI PSK, ATLET_GANDA AG
        WHERE PPK.jenis_partai = PK.jenis_partai
        AND PPK.nama_event = PK.nama_event
        AND PPK.tahun_event = PK.tahun_event
        AND PPK.Nomor_Peserta = PSK.Nomor_Peserta
        AND PSK.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
        AND PPK.nama_event = %s
        AND PPK.tahun_event = %s)
    );
    """
    cursor.execute(query_get_available_atlet_ganda, (athlete_id, nama_event, tahun_event, nama_event, tahun_event))
    available_atlet_ganda = cursor.fetchall()
    return available_atlet_ganda

def get_stadium(nama_stadium, cursor):
    query_get_stadium = """
    SELECT * FROM STADIUM S
    WHERE S.nama = %s
    """    
    cursor.execute(query_get_stadium, (nama_stadium,))
    data_stadium = cursor.fetchone()
    return data_stadium

def get_event(nama_event, tahun_event, cursor):
    query_get_event = """
    SELECT * FROM EVENT E
    WHERE E.nama_event = %s
    AND E.tahun = %s
    """
    cursor.execute(query_get_event, (nama_event, tahun_event))
    data_event = cursor.fetchone()
    data_event = (data_event[0], data_event[1], data_event[2], data_event[3], 
                  data_event[4].strftime('%d-%m-%Y'), data_event[5].strftime('%d-%m-%Y'), 
                  data_event[6], locale.currency(data_event[7], grouping=True))
                  
    return data_event

def get_event_in_stadium(nama_stadium, cursor):
    query_get_event = """
    SELECT E.nama_event, E.Total_hadiah, E.Tgl_mulai, E.Kategori_Superseries, E.Tahun
    FROM EVENT E
    WHERE E.nama_stadium = %s
    AND E.Tgl_Mulai > CURRENT_DATE
    """
    event_list = cursor.execute(query_get_event, (nama_stadium,))
    event_list = cursor.fetchall()
    event_list = [(event[0], locale.currency(event[1], grouping=True), 
                   event[2].strftime('%d-%m-%Y'), event[3], event[4]) for event in event_list]
                   
    return event_list