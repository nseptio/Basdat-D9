from django.shortcuts import render, redirect
from utils.query import *
from django.http import HttpRequest

# Create your views here.

def fetch_data(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# def show_latih_atlet(request):
#     query = """
#     SELECT M.Name FROM MEMBER M, ATLET A WHERE M.ID=A.ID;
#     """
#     cursor.execute(query)
#     daftar_atlet_untuk_dipilih = fetch_data(cursor)
    
#     context = {'daftar_atlet_untuk_dipilih' : daftar_atlet_untuk_dipilih}

#     return render(request, "latih_atlet.html", context)

def show_list_atlet_dilatih(request):
    email_pelatih = request.COOKIES.get("email")
    query = """SELECT MA.Name, MA.Email, A.World_rank
                FROM MEMBER MA, MEMBER MP, ATLET A, ATLET_PELATIH AP, PELATIH P 
                WHERE MA.ID=A.ID
                AND MP.ID=P.ID
                AND AP.ID_Pelatih=P.ID
                AND AP.ID_Atlet=A.ID
                AND MP.Email='{}';
                """.format(email_pelatih)
    cursor.execute(query)
    daftar_atlet_dilatih = fetch_data(cursor)

    context = { "daftar_atlet_dilatih" : daftar_atlet_dilatih}
    return render(request, "list_atlet_dilatih.html", context)

def show_latih_atlet (request):
    if request.method == 'POST':
        email_pelatih = request.COOKIES.get("email")
        id_atlet = request.POST.get("athlete-select")
    
        query = """
                SELECT ID FROM MEMBER WHERE EMAIL = '{email_pelatih}';
                """
        cursor.execute(query)
        id_pelatih = fetch_data(cursor)

        if id_atlet:
            query2 = """
                    INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
                    """
            cursor.execute(query2)
            return redirect("list_atlet_dilatih/")
        
    query3 = """
    SELECT M.Name, M.id 
    FROM MEMBER M, ATLET A 
    WHERE M.ID=A.ID 
    ORDER BY M.name;
    """
    cursor.execute(query3)
    list_nama_id_atlet = fetch_data(cursor)
    context = {
        "list_nama_id_atlet": list_nama_id_atlet
    }

    return render(request, 'latih_atlet.html', context)



