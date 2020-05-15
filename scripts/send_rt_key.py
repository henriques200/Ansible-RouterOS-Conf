#!/usr/bin/python3
#-*- coding: utf-8 -*-

import pexpect

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
