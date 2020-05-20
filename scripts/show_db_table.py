#!/usr/bin/python3

import psycopg2

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mikrotik")

    cursor = connection.cursor()
    # Fetch all data from table
    cursor.execute("SELECT * from routers;")
    record = cursor.fetchall()
    # print("Output data:", record)
    for output in record:
        print(output)


except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
