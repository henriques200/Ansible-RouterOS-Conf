#!/usr/bin/python3
# -*- coding:utf-8 -*-
 
import sys 
import psycopg2 
import os 


# Start PostgresSQL connection
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mikrotik")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    sys.exit() 


def mostrar_tabela():
        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT * FROM comandos_mikrotik"
        cursor.execute(postgreSQL_select_Query)
        get_info = cursor.fetchall()
        # Prints the selected table contents
        print("Tabela:")
        for row in get_info:
            print("ID:", row[0]) 
            print("Comando:", row[1]) 
            print("Descricao:", row[2], "\n") 


def get_all_commands():
        '''
        get_all_commands()
        > Prints all commands saved on the DB.
        '''
        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT comando FROM comandos_mikrotik"
        cursor.execute(postgreSQL_select_Query)
        all_commands = cursor.fetchall()
        # Prints all commands stored saved on the DB.
        print("Comandos guardados na Base de Dados:")
        for row in all_commands:
            for command in row:
                print(">", command)

    
def search_id_command(id_list, write_to_file = 0):
    '''
    search_id_command(id_list, write_to_file = 0)
    > Returns multiple mikrotik commands
    based on the number of IDs to lookup.
    > id_list - requires a list of numbers.
    Those numbers has to be strings.
    eg.: ["1", "2"]
    > write_to_file - is an optional variable
    but if used has to be a integer.
    0 - Default. Does not write to a file.
    1 - Enabled. Writes to a file multiple commands.
    > Returns a list containing multiple commands.
    '''
    commands = []
    cursor = connection.cursor()
    # Fetch all data from table
    for data in id_list:
        sql_query = ("SELECT comando FROM comandos_mikrotik WHERE id IN (%s)")
        cursor.execute(sql_query, data)
        record = cursor.fetchone()
        if(record != None):
            for command_out in record:
                commands.append(command_out)
        else:
            # Adds a message reporting that the id does not exists.
            commands.append("ID {} nao existe!".format(data))
    if(write_to_file == 1):
        print("Comandos escritos para o ficheiro commands.txt")
        file = open('commands.txt', 'w')
        for data in commands:
            file.write(data + '\n')
        file.close()
    return commands


def description(desc):    
        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT * FROM comandos_mikrotik WHERE descricao=%s"
        data = (desc,)
        cursor.execute(postgreSQL_select_Query, data)
        
        get_info = cursor.fetchall()
        for row in get_info:
            print("ID: ", row[0])
            print("Comando: ", row[1])
            print("Descricao: ", row[2], "\n")

 
def menu():
    while(True):
        print("****MAIN MENU****")
        choice = input("""
A: Mostrar tabela toda
B: Ver todos os comandos
C: Mostrar descricoes
E: Escolher o ID e mandar os comandos para o .txt
S: Sair

Escolha uma das opcoes: """)
        os.system('clear')
        if(choice == "A" or choice == "a"):
            mostrar_tabela()
        elif(choice == "B" or choice == "b"):
            get_all_commands()
        elif(choice == "C" or choice == "c"):
            print("Descricoes Disponiveis que pode escolher: ip")
            desc = input("Insira a descricao para obter os comandos: ")
            description(desc)
        elif(choice == "E" or choice == "e"):
            numb_list = []
            while(True):
                numb = input("Introduz um numero: ")
                if(numb in numb_list):
                    print("O numero ja existe! Tenta de novo.")
                else:
                    numb_list.append(numb)
                    option = input("Queres continuar? (s/n): ")
                    if(option == "N" or option == "n"):
                       break
            search_id_command(numb_list, 1)
        elif(choice == "S" or choice == "s"):
            break
        else:
            print("Deve apenas escolher uma das opcoes A,B,C,D,S.") 


if (__name__ == '__main__'):
    menu()
