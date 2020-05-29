#!/usr/bin/python3
# -*- coding:utf-8 -*-

import psycopg2


def get_command(descricao):
    '''
    get_command(descricao)
    > Returns a string with the mikrotik command
      asked by the user.
    > Returns None and a print error if the connection
      is not well configured.
    > descricao var is the command description.
      String required.
    '''
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "123",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "mikrotik")

        cursor = connection.cursor()
        # Execute the sql_query with the data required
        sql_query = "SELECT * from comandos_mikrotik WHERE descricao = %s"
        data = (descricao, )
        cursor.execute(sql_query, data)
        # Fetch the output and return it
        record = cursor.fetchone()
        output = record[1]
        return output
    except (Exception, psycopg2.Error) as error :
        print("Error while connecting to PostgreSQL", error)
        return None
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def get_all_commands():
    '''
    get_all_commands()
    > Returns a list with all the mikrotik commands
      available on the DB.
    > Returns None and a print error if the connection
      is not well configured.
    '''
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "123",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "mikrotik")

        cursor = connection.cursor()
        # Execute the sql_query with the data required
        cursor.execute("SELECT comando from comandos_mikrotik")
        # Fetch the output and return it
        record = cursor.fetchall()
        output = []
        # Convert list of tuples to a list
        for t in record:
            for x in t:
                output.append(x)
        return output
    except (Exception, psycopg2.Error) as error :
        print("Error while connecting to PostgreSQL", error)
        return None
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()



if(__name__ == '__main__'):
    '''
    comando = get_command("Nota do sistema")
    print(comando)
    '''
    print(get_all_commands())
