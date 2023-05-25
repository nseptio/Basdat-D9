from django.shortcuts import render, redirect
from utils.query import *
from django.http import HttpRequest
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def fetch_data(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_list_atlet_dilatih(request):
    email_pelatih = request.COOKIES.get("email")
    query = f"""
            SELECT DISTINCT MAT.Name, MAT.Email, A.World_rank
	        FROM ATLET A, MEMBER M, ATLET_PELATIH AP, MEMBER MPEL, MEMBER MAT
	        WHERE MPEL.Email LIKE '{email_pelatih}'
	        AND MPEL.ID = AP.ID_PELATIH
	        AND AP.ID_ATLET = A.ID
	        AND A.ID = MAT.ID;
            """
    
    cursor.execute(query)
    daftar_atlet_dilatih = fetch_data(cursor)

    print (email_pelatih)
    print(daftar_atlet_dilatih)

    context = { "daftar_atlet_dilatih" : daftar_atlet_dilatih}
    return render(request, "list_atlet_dilatih.html", context)

def show_latih_atlet (request):
    if request.method == 'POST':
        email_pelatih = request.COOKIES.get("email")
        id_atlet = request.POST.get("athlete-select")
        
        query = f"""
                SELECT ID 
                FROM MEMBER 
                WHERE Email LIKE '{email_pelatih}';
                """
        cursor.execute(query)
        id_pelatih = fetch_data(cursor)[0]['id']

        if id_atlet:
            query2 = f"""
                    INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
                    """
            cursor.execute(query2)
            return redirect("/list_atlet_dilatih")
        
    query3 = """
    SELECT M.Name, M.ID 
    FROM MEMBER M, ATLET A 
    WHERE M.ID = A.ID 
    ORDER BY M.Name;
    """
    cursor.execute(query3)
    list_nama_id_atlet = fetch_data(cursor)
    context = {
        "list_nama_id_atlet": list_nama_id_atlet
    }

    return render(request, 'latih_atlet.html', context)



