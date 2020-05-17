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
    # Run ping command to check host is alive
    ping = subprocess.run(['ping', '-c 2', ip], stdout=subprocess.PIPE)
    output_ping = ping.stdout.decode("utf-8")
    # Prints an error if ping fails
    if(output_ping.find("100% packet loss")):
        print("ERRO - IP {} nao esta disponivel!".format(ip))
    else:
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
