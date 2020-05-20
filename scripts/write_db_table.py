#!/usr/bin/python3

import psycopg2

print("Escrever dados na Tabela.")
cidade = input("Introduz a cidade: ")
rua = input("Introduz a rua: ")
cod_postal = input("Introduz o codigo postal: ")
empresa = input("Introduz o nome da empresa: ")
nome_maquina = input("Introduz o nome da maquina: ")
ip_nome = input("Introduz o IP ou nome: ")

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mikrotik")

    cursor = connection.cursor()
    # Creates a SQL query
    sql_query = "INSERT INTO routers " \
                "(cidade, rua, codigo_postal, empresa, nome_maquina, ip_nome) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
    # Fetch data
    data = (cidade, rua, cod_postal, empresa, nome_maquina, ip_nome)
    # Execute the query with the data
    cursor.execute(sql_query, data)
    print(sql_query)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    # Closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
