#!/usr/bin/python3
#-*- coding: utf-8 -*-

import pexpect
import subprocess

'''
Put remote IPs in ip.txt file or change the file name.
Copy ip addresses from txt file and send ssh commands
  to the remote machines. 
'''

# Fetch the ip list
ip_file = open("ip.txt")
ip_list = ip_file.read().splitlines()
ip_file.close()

for ip in ip_list:
    # Build the ssh command
    ssh_command = "ssh admin@{}".format(ip)
    # Test the command and send the key
    try:
        ssh = pexpect.spawn(ssh_command)
        ssh.expect(' (yes/no)?')
        ssh.sendline('yes')
        ssh.expect('] >')
        ssh.sendline('quit')
        print("{} OK!".format(ip))
    except:
        # Print an error if ssh fails
        print("Erro com o IP {}!".format(ip))
