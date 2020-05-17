#!/usr/bin/python3
#-*- coding: utf-8 -*-

import pexpect
import subprocess

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
    ping = subprocess.run(['ping', '-c 2', ip], stdout=subprocess.PIPE)
    output_ping = ping.stdout.decode("utf-8")
    if(output_ping.find("100% packet loss")):
        print("ERRO - IP {} nao esta disponivel!".format(ip))
    else:
        try:
            ssh = pexpect.spawn(ssh_command)
            ssh.expect(' (yes/no)?')
            ssh.sendline('yes')
            ssh.expect('] >')
            ssh.sendline('quit')
            print("{} OK!".format(ip))
        except:
            print("Erro com o IP {}!".format(ip))
