#!/usr/bin/python3
# -*- coding:utf-8 -*-
 
import sys 
import psycopg2 
import os 
import json
# Start PostgresSQL connection
try:
    connection = psycopg2.connect(user = "root",
                                  password = "123",
                                  host = "192.168.56.118",
                                  port = "5432",
                                  database = "mikrotik") 
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    sys.exit() 
def show_table(returns_table = 0):
    '''
    show_table(returns_table = 0)
    > Returns all the table content. returns_table - is an optional variable
    but if used has to be a integer.
    0 - Default. Prints the table content.
    1 - Enabled. Returns a tuple containing all the table
    contents but does not print the table content.
    '''
    table_list = []
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM comandos_mikrotik"
    cursor.execute(postgreSQL_select_Query)
    get_info = cursor.fetchall()
    if(returns_table == 1):
        for row in get_info:
            line = (row[0], row[1], row[2])
            '''
            for data in row:
                line.append(data)
            '''
            table_list.append(line)
        table = tuple(table_list)
        return table
    else:
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
    0 - Default. Does not write to a file and returns
    a list containing multiple commands.
    1 - Enabled. Writes to a file multiple commands.
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
def search_description(desc):
    '''
    search_description(desc)
    > Search info based on the
    description.
    > desc - required variable.
    Has to be a string.
    > Prints the result information.
    '''
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM comandos_mikrotik WHERE descricao=%s"
    data = (desc,)
    cursor.execute(postgreSQL_select_Query, data)
    get_info = cursor.fetchall()
    for row in get_info:
        print("ID: ", row[0])
        print("Comando: ", row[1])
        print("Descricao: ", row[2], "\n") 
def get_hosts(ids_list):
    hosts = []
    cursor = connection.cursor()
    for ids in ids_list:
        sql_query = ("SELECT ip_address FROM clientes WHERE id = %s")
        data = (ids)
        cursor.execute(sql_query, data)
        # Fetch all IP addresses and save to a list
        record = cursor.fetchone()
        for ip in record:
            hosts.append(ip)
    # Creates the inventory dictionary
    inv_dictionary = {
    "routeros": {
      "hosts": hosts,
      "vars": {
        "ansible_network_os": "routeros",
        "ansible_user": "admin",
        "ansible_password": "",
        "ansible_connection": "network_cli"
      }
     }
    }
    # Converts to JSON format
    ansible_inventory = json.dumps(inv_dictionary)
    f = open('/etc/ansible/table.json', 'w')
    json.dump(ansible_inventory, f)
    f.close()

def insert_commands(comando, descricao):
    cursor = connection.cursor()
    sql_query = "INSERT INTO comandos_mikrotik (comando, descricao) VALUES (%s, %s)"
    data = (comando, descricao)
    cursor.execute(sql_query, data)
    connection.commit()

def remove_commands(remover):
    cursor = connection.cursor()
    sql_query = "DELETE FROM comandos_mikrotik WHERE id = %s"
    data = (remover)
    cursor.execute(sql_query, data)
    connection.commit()
    
 
def menu():
    while(True):
        print("****MAIN MENU****")
        choice = input(""" 
                           A: Mostrar tabela toda 
                           B: Ver todos os comandos 
                           C: Mostrar descricoes 
                           E: Escolher o ID e mandar os comandos para o .txt 
                           F: Escolher o ID e mandar os IPs para o inventario
                           G: Inserir comandos na base de dados
                           H: Remover comandos da base de dados 
                           S: Sair Escolha uma das opcoes: """)
        os.system('clear')
        if(choice == "A" or choice == "a"):
            show_table()
        elif(choice == "B" or choice == "b"):
            get_all_commands()
        elif(choice == "C" or choice == "c"):
            print("Descricoes Disponiveis que pode escolher: ip")
            desc = input("Insira a descricao para obter os comandos: ")
            search_description(desc)
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
        elif(choice == "F" or choice == "f"):
            ids_list = []
            print("Introduza os IDs para usar os IPs")
            while(True):
                numb = input("Introduz um numero: ")
                if(numb in ids_list):
                    print("O numero ja existe! Tenta de novo.")
                else:
                    ids_list.append(numb)
                    option = input("Queres continuar? (s/n): ")
                    if(option == "N" or option == "n"):
                        break
            get_hosts(ids_list)
        elif(choice == "G" or choice == "g"):
            while(True):
                comando = input("Introduza o comando: ")
                descricao= input("Introduza uma descricao: ")            
                option = input("Queres continuar? (s/n): ")
                if(option == "N" or option == "n"):
                    break
            insert_commands(comando, descricao)
        elif(choice == "H" or choice == "h"):
            while(True):
                remover = input("Introduza o ID do comando: ")            
                option = input("Queres continuar? (s/n): ")
                if(option == "N" or option == "n"):
                    break
            remove_commands(remover)
        
        elif(choice == "S" or choice == "s"):
            break
        else:
            print("Deve apenas escolher uma das opcoes A,B,C,D,S.") 
if (__name__ == '__main__'):
    menu()
