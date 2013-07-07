#!/usr/bin/env python

'''Air Codea
Shell interface for the 'Air Code' feature of Codea

Usage:
  codea [-r]
  codea [-r] push <name>
  codea [-r] pull <name>

Options:
  -h --help     Show this help
  -r --restart  Restart the project

'''

import requests as req
from lxml import html
import json
from ConfigParser import ConfigParser
from hashlib import md5
from docopt import docopt


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
        # FIXME strip .lua if there
        text = open(filename + '.lua').read()
        req.post(self.base + '/__update',
            data=json.dumps({
                'file': filename,
                'contents': text
            })
        )
        return md5(text).hexdigest()

    def download_file(self, filename):
        # FIXME strip .lua if there
        resp = req.get('%s/%s' % (self.base, filename))
        xp = '//div[@id="editor"]'
        text = html.fromstring(resp.content).xpath(xp)[0].text
        open(filename + '.lua', 'w').write(text)
        return md5(text).hexdigest()

    def restart(self):
        req.get(self.base + '/__restart')


args = docopt(__doc__)
cfg = ConfigParser()
cfg.read('.air_codea.cfg')
# I can do **dict(cfg.items('connection')) or similar... but what errors?
ip = cfg.get('connection', 'ip')
port = cfg.get('connection', 'port')
project = cfg.get('connection', 'project')
cp = CodeaProject(ip, port, project)


if args['push']:
    cp.upload_file(args['<name>'])
elif args['pull']:
    cp.download_file(args['<name>'])
else:
    print 'coming soon'

if args['--restart']:
    cp.restart()
