#!/usr/bin/python3

import psycopg2

def getTableInfo(ZipCode):
    try:
       connection = psycopg2.connect(user="postgres",
                                     password="123",
                                     host="192.168.0.104",
                                     port="5432",
                                     database="postgres"
                                    )
   
       print("\n")
       print("########## PostgresSQL connection is open ########## \n")
       cursor = connection.cursor()
       postgreSQL_select_Query = "SELECT * FROM clientes WHERE codigo_postal = %s"
       data = (ZipCode, )

       cursor.execute(postgreSQL_select_Query, data)
       get_info = cursor.fetchall() 
       print("Information: \n")
       for row in get_info:
          print("Info = ", row,"\n")
       
       ip = row[6]
       print("Ip Address= ", ip)

    except (Exception, psycopg2.Error) as error :
       print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
           cursor.close()
           connection.close()
           print("\n")
           print("########## PostgreSQL connection closed ########## \n")


ZipCode = input("Insira o Codigo Postal: \n")
getTableInfo(ZipCode)
