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
from ConfigParser import ConfigParser, NoSectionError
from hashlib import md5
from docopt import docopt
from glob import glob


class CodeaProject(object):
    def __init__(self, ip, port, project):
        self.base = 'http://%s:%s/projects/%s' % (ip, port, project)
        # Always make sure we are on the right project
        self._check_files()

    def _check_files(self):
        resp = req.get(self.base)
        xp = '//ul[@class="tabs"]/a[@href!="/"]/li'
        files = [e.text for e in html.fromstring(resp.content).xpath(xp)]
        self.files = files
        print files

    def upload_file(self, filename):
        text = open(filename + '.lua').read()
        req.post(self.base + '/__update',
            data=json.dumps({
                'file': filename,
                'contents': text
            })
        )
        return md5(text).hexdigest()

    def get_file(self, filename):
        resp = req.get('%s/%s' % (self.base, filename))
        xp = '//div[@id="editor"]'
        text = html.fromstring(resp.content).xpath(xp)[0].text
        return md5(text).hexdigest(), text

    def download_file(self, filename):
        code_hash, text = self.get_file(filename)
        open(filename + '.lua', 'w').write(text)
        return code_hash

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

filename = args['<name>']
if filename is not None and filename.endswith('.lua'):
    filename = filename[:-4]


def save_hash(filename, code_hash):
    if not cfg.has_section(filename):
        cfg.add_section(filename)
    cfg.set(filename, 'hash', code_hash)


# Push
if args['push']:
    if filename in cp.files:
        code_hash = cp.upload_file(filename)
        save_hash(filename, code_hash)
    else:
        print 'That file is not in the project!'

# Pull
elif args['pull']:
    code_hash = cp.download_file(filename)
    save_hash(filename, code_hash)

# Sync
else:
    local_files = [f[:-4] for f in glob('*.lua')]
    for fn in cp.files:
        # Remote file is not Local
        if fn not in local_files:
            print 'Downloading', fn
            save_hash(fn, cp.download_file(fn))
            continue

        # We don't have a hash on file
        try:
            last_hash = cfg.get(fn, 'hash')
        except NoSectionError:
            print 'Unknown state for', fn
            continue

        # Get local details
        local_text = open(fn + '.lua').read()
        local_hash = md5(local_text).hexdigest()

        # No local changes, might as well download
        if local_hash == last_hash:
            print 'Downloading (unchanged locally)', fn
            save_hash(fn, cp.download_file(fn))
            continue

        # We have to download the remote now
        remote_hash, remote_text = cp.get_file(fn)

        # If the remote is unchanged then upload
        if remote_hash == last_hash:
            print 'Uploading', fn
            save_hash(fn, cp.upload_file(fn))
            continue

        print 'Local and remote changed for', fn

if args['--restart']:
    print 'Restarting'
    cp.restart()

cfg.write(open('.air_codea.cfg', 'wb'))
