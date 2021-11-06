import psycopg2
from psycopg2 import Error, connect

try:
    connection = psycopg2.connect(user="postgres", password="2020", database="project")

    # create a cursor to perform database operations
    cursor = connection.cursor()

    # print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    # executing an SQL query
    # cursor.execute("SELECT version();")
    cursor.execute("\d;")

    # fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgresSQL", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
