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
    
    # Test
    # cursor.execute(f"""
    # SELECT S.nama_brand
    # FROM SPONSOR S
    # WHERE S.id NOT IN (
    #     SELECT id_sponsor
    #     FROM ATLET_SPONSOR ATS
    #     JOIN ATLET A ON A.id = ATS.id_atlet
    #     NATURAL JOIN MEMBER M
    #     WHERE M.email = 'kballeinea@dell.com'
    # );
    # """)
    # record = cursor.fetchall()
    # print(record, type(record), type(record[0]))
    # list_sponsor = [i[0] for i in record]
    # print(list_sponsor)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
