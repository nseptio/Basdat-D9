import psycopg2
from psycopg2 import Error

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="ywbaKGJV9lDcyLP9inLc",
                                  host="containers-us-west-108.railway.app",
                                  port="6771",
                                  database="railway")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    
    cursor.execute("SELECT name, tanggal_mulai, spesialisasi FROM MEMBER M NATURAL JOIN PELATIH P JOIN PELATIH_SPESIALISASI PS ON " +
                   "P.id = PS.id_pelatih JOIN SPESIALISASI S ON PS.id_spesialisasi = S.id WHERE M.email = 'ifassam6@yolasite.com';")
    hasil = cursor.fetchall()
    kategori = []
    for i in hasil:
        kategori.append(i[2])
    print(hasil)
    print(kategori)
    
#     SELECT name, tanggal_mulai, spesialisasi FROM MEMBER M NATURAL JOIN PELATIH P JOIN PELATIH_SPESIALISASI PS ON
# P.id = PS.id_pelatih JOIN SPESIALISASI S ON PS.id_spesialisasi = S.id WHERE M.email = 'ifassam6@yolasite.com';


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
