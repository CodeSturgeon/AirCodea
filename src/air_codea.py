import requests as req
from lxml import html
import json
from hashlib import md5
import logging
from time import sleep

log = logging.getLogger('base')

UPDATE_PAUSE_TIME = 2

class CodeaProject(object):
    def __init__(self, ip, port, project):
        self.base = 'http://%s:%s/projects/%s' % (ip, port, project)
        # Always make sure we are on the right project
        self._check_files()
        self.uploaded = False

    def _check_files(self):
        log.info('Checking files @ %s' % self.base)
        resp = req.get(self.base)
        if resp.status_code!= 200:
            log.debug(resp.content)
        xp = '//ul[@class="tabs"]/a[@href!="/"]/li'
        files = [e.text for e in html.fromstring(resp.content).xpath(xp)]
        self.files = files
        log.info('Found %s' % ', '.join(files))

    def upload_file(self, filename):
        log.info('Uploading %s' % filename)
        if self.uploaded:
            sleep(UPDATE_PAUSE_TIME)
        text = open(filename + '.lua').read()
        resp = req.post(self.base + '/__update',
            data=json.dumps({
                'file': filename,
                'contents': text
            })
        )
        if resp.status_code!= 200:
            log.debug(resp.content)
        self.uploaded = True
        return md5(text).hexdigest()

    def get_file(self, filename):
        log.info('Getting %s' % filename)
        resp = req.get('%s/%s' % (self.base, filename))
        if resp.status_code!= 200:
            log.debug(resp.content)
        xp = '//div[@id="editor"]'
        text = html.fromstring(resp.content).xpath(xp)[0].text
        if text is None:  # Blank file
            log.info('Got blank file')
            text = ''
        return md5(text).hexdigest(), text

    def download_file(self, filename):
        code_hash, text = self.get_file(filename)
        open(filename + '.lua', 'w').write(text)
        return code_hash

    def restart(self):
        log.info('Restarting')
        if self.uploaded:
            sleep(UPDATE_PAUSE_TIME)
        resp = req.get(self.base + '/__restart')
        if resp.status_code!= 200:
            log.debug(resp.content)
