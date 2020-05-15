#!/usr/bin/python3
#-*- coding: utf-8 -*-

import pexpect

'''
Put remote IPs in ip.txt file or change the file name.
Copy ip addresses from txt file and send ssh commands
  to the remote machines. 
'''

ip_file = open("ip.txt")
ip_list = ip_file.read().splitlines()
ip_file.close()

for ip in ip_list:
    ssh_command = "ssh admin@{}".format(ip)
    try:
        ssh = pexpect.spawn(ssh_command)
        ssh.expect(' (yes/no)?')
        ssh.sendline('yes')
        ssh.expect('] >')
        ssh.sendline('quit')
        print("{} OK!".format(ip))
    except:
        print("Erro com o IP {}!".format(ip))
