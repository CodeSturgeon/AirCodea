#!/usr/bin/env python
import requests as req
from lxml import html
import json

ip = '192.168.1.6'
port = '42000'
project = 'Synkit'
base = 'http://%s:%s/projects/%s' % (ip, port, project)

main = open('Main.lua').read()

req.get(base)

d = json.dumps({'file':'Main', 'contents':main})
print d
u = req.post(base+'/__update', data=d)
