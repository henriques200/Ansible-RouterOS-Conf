#!/usr/bin/python3
# -*- coding:utf-8 -*-

import psycopg2
import json

# Start PostgresSQL connection
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "192.168.0.104",
                                  port = "5432",
                                  database = "postgres")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)


def get_hosts(id_list):
    hosts = []
    cursor = connection.cursor()
    for ids in id_list:
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
    f = open('table.json', 'w')
    json.dump(ansible_inventory, f)   
    f.close()   
    #return(ansible_inventory)
    

if(__name__ == '__main__'):
    id_list = []
    while(True):
        numb = input("Introduz um numero: ")
        if(numb in id_list):
            print("O numero ja existe! Tenta de novo.")
        else:
            id_list.append(numb)
            option = input("Queres continuar? (s/n): ")
            if(option == "N" or option == "n"):
                break
    
    print(get_hosts(id_list))
