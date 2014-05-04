from hashlib import md5
import logging
from splinter import Browser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from time import sleep

SYNTAX_SLEEP_TIME = 0.5
UPLOAD_SLEEP_TIME = 2

log = logging.getLogger('base')


class CodeaException(Exception):
    pass


class CodeaProject(object):
    def __init__(self, ip, port, project):
        self.base = 'http://%s:%s/projects/%s' % (ip, port, project)
        # FIXME set a low timeout or somehow test the base string first
        self.browser = Browser('phantomjs')

        self.uploaded = False

        # Always make sure we are on the right project
        self._check_files()

    def _check_files(self):
        log.info('Checking files @ %s' % self.base)
        self.browser.visit(self.base)
        # FIXME check return code
        xp = '//ul[@class="tabs"]/a[@href!="/"]/li'
        files = [e.text for e in self.browser.find_by_xpath(xp)]
        self.files = files
        log.info('Found %s' % ', '.join(files))

    def upload_file(self, filename):
        log.info('Uploading %s' % filename)

        # Navigate to page if needed
        page_url = '%s/%s' % (self.base, filename)
        if self.browser.url != page_url:
            self.browser.visit(page_url)
            # FIXME check return code

        if self.uploaded:
            # Just give Codea a chance to catch up
            log.debug('Quick snooze to avoid timing problems')
            sleep(UPLOAD_SLEEP_TIME)

        text = open(filename + '.lua').read()
        quoted_text = text.encode('string_escape')
        js = "editor.setValue('%s')" % quoted_text
        self.browser.execute_script(js)

        # Wait to for the ACE editor to catch up
        sleep(SYNTAX_SLEEP_TIME)

        # Check that AirCode/ACE likes what we gave it
        try:
            js = 'editor.getSession().getAnnotations()[0].text'
            ret = self.browser.evaluate_script(js)
        except WebDriverException:
            # If the JS can't find annotations there are no problems found
            self.uploaded = True
            pass
        else:
            # An annotation describing a problem is present on the page
            err = "%s failed to upload due to error: %s" % (filename, ret)
            log.error(err)
            raise CodeaException(err)

        return md5(text).hexdigest()

    def get_file(self, filename):
        log.info('Getting %s' % filename)
        self.browser.visit('%s/%s' % (self.base, filename))
        # FIXME check return code
        text = self.browser.evaluate_script('editor.getSession().getValue()')
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
            # Just give Codea a chance to catch up
            log.debug('Quick snooze to avoid timing problems')
            sleep(UPLOAD_SLEEP_TIME)

        self.browser.find_by_css('.ace_text-input')[0].type(Keys.CONTROL + 'r')
