#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json

file = open('table.json', 'r')
data = file.read()
print(json.loads(data))
file.close()

#print(data)
