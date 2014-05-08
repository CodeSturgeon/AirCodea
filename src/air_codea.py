import requests as req
from lxml import html
import json
from hashlib import md5
import logging
from time import sleep

log = logging.getLogger('base')

UPDATE_PAUSE_TIME = 0.1  # NOTE: might have to scale this up for big files
TIMEOUT = 0.5


class CodeaProject(object):
    def __init__(self, ip, port, project):
        self.base = 'http://%s:%s/projects/%s' % (ip, port, project)
        # Always make sure we are on the right project
        self._check_files()

    def _check_files(self):
        log.info('Checking files @ %s' % self.base)
        resp = req.get(self.base, timeout=TIMEOUT)
        if resp.status_code != 200:
            log.debug(resp.content)
        xp = '//ul[@class="tabs"]/a[@href!="/"]/li'
        files = [e.text for e in html.fromstring(resp.content).xpath(xp)]
        self.files = files
        log.info('Found %s' % ', '.join(files))

    def upload_file(self, filename):
        log.info('Uploading %s' % filename)
        text = open(filename + '.lua').read()
        resp = req.post(self.base + '/__update', timeout=TIMEOUT,
            data=json.dumps({
                'file': filename,
                'contents': text
            })
        )
        if resp.status_code != 200:
            log.debug(resp.content)

        # Give AirCode some breathing room to prevent crashes
        sleep(UPDATE_PAUSE_TIME)

        # Check to see if the upload worked
        # AirCode will reject text with syntax errors
        check_text = self.get_file(filename)[1]
        # Always be sure to track what is in Codea
        text = check_text

        return md5(text).hexdigest()

    def get_file(self, filename):
        log.info('Getting %s' % filename)
        resp = req.get('%s/%s' % (self.base, filename), timeout=TIMEOUT)
        if resp.status_code != 200:
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
        resp = req.get(self.base + '/__restart')
        if resp.status_code != 200:
            log.debug(resp.content)
