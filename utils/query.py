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

    cursor.execute("SELECT * FROM MEMBER")
    record = cursor.fetchall()
    for i in record:
        print(i)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
