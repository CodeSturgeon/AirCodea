import requests as req
from lxml import html
import json
from hashlib import md5


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
        if text is None:  # Blank file
            text = ''
        return md5(text).hexdigest(), text

    def download_file(self, filename):
        code_hash, text = self.get_file(filename)
        open(filename + '.lua', 'w').write(text)
        return code_hash

    def restart(self):
        req.get(self.base + '/__restart')
