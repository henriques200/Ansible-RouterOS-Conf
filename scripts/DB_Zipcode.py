#!/usr/bin/python3

import psycopg2
import operator

codigo = input("Insira o Codigo Postal: ")
query = ("SELECT * FROM table_test WHERE codigo_postal = '%s'" % codigo)
try:
   connection = psycopg2.connect(user="postgres",
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="DBTeste")
   cursor = connection.cursor()
   cursor.execute(query)
   info_records = cursor.fetchall()
   
   for row in info_records:
       print ("CODIGO-POSTAL-> ", row[3], "LOJA-> ", row[4], "IP-> ", row[5], "MARCA-> ", row[6])

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
