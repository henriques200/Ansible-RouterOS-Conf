#!/usr/bin/python3
# -*- coding:utf-8 -*-

import psycopg2
import json

# Start PostgresSQL connection
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mikrotik")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)


def get_hosts():
    hosts = []
    cursor = connection.cursor()
    # All IPs from a table
    sql_query = ("SELECT ip_nome FROM routers")
    cursor.execute(sql_query, )
    # Fetch all IP addresses and save to a list
    record = cursor.fetchall()
    for result in record:
        for ip in result:
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
    # print(ansible_inventory)
    return ansible_inventory


if(__name__ == '__main__'):
    print(get_hosts()) 
