#!/usr/bin/env python
import requests as req
from lxml import html
import json
from ConfigParser import ConfigParser


class CodeaProject(object):
    def __init__(self, ip, port, project):
        self.base = 'http://%s:%s/projects/%s' % (ip, port, project)
        # Always make sure we are on the right project
        self._check_files()

    def _check_files(self):
        # FIXME error checking
        resp = req.get(self.base)
        xp = '//div[@class="project-title"]'
        files = [e.text for e in html.fromstring(resp.content).xpath(xp)]
        self.files = files

    def upload_file(self, filename):
        # FIXME check for file exsistance
        text = open(filename+'.lua').read()
        resp = req.post(self.base+'/__update',
            data=json.dumps({
                'file': filename, 
                'contents': text
            })
        )

    def download_file(self, filename):
        resp = req.get('%s/%s' % (self.base, filename))
        xp = '//div[@id="editor"]'
        text = html.fromstring(resp.content).xpath(xp)[0].text
        open(filename+'.lua', 'w').write(text)

    def restart(self):
        resp = req.get(self.base+'/__restart')

cfg = ConfigParser()
cfg.read('.air_codea.cfg')
# I can do **dict(cfg.items('connection')) or similar... but what errors?
ip = cfg.get('connection', 'ip')
port = cfg.get('connection', 'port')
project = cfg.get('connection', 'project')

cp = CodeaProject(ip, port, project)
cp.upload_file('Main')
cp.download_file('Joe')
cp.restart()
