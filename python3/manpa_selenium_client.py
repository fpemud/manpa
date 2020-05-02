#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

# manpa_selenium_client.py -
#
# Copyright (c) 2019-2020 Fpemud <fpemud@sina.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated DocTemplation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import time
import random
import selenium
from manpa_util import ManpaUtil


"""
ManpaSeleniumWebDriver is similar but not compatible with Selenium WebDriver.
You can always get the WebDriver object by .driver property.
"""


class ManpaSeleniumWebDriver(selenium.webdriver.Chrome):

    def __init__(self, parent, downloadDir):
        self.parent = parent
        self.parent.seleniumClientList.append(self)

        self.downloadDir = downloadDir
        self.driver = None

        try:
            # select User-Agent
            ua = ManpaUtil.getRandomUserAgent()

            # select google-chrome options
            options = []
            if True:
                options = selenium.webdriver.chrome.options.Options()
                options.add_argument('--no-sandbox')                    # FIXME
                if ua is not None:
                    options.add_argument('user-agent=' + ua)
                # options.add_argument('--proxy-server=http://ip:port')

            # select google-chrome preferences
            prefs = dict()
            if True:
                # enable download capabilities
                prefs.update({
                    "download.default_directory": self.downloadDir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": False,
                    "safebrowsing.disable_download_protection": True,
                })

            # create webdriver object
            options.add_experimental_option("prefs", prefs)
            super().__init__(options=options)
        except Exception:
            self.quit()
            raise

    def quit(self):
        super().quit()
        if True:
            self.downloadDir = None
        if True:
            self.parent.seleniumClientList.remove(self)
            self.parent = None

    def get(self, url):
        super().get(url)
        time.sleep(random.randrange(5, 10))

    def click_and_wait(self, elem):
        self.click()
        time.sleep(random.randrange(5, 10))

    def retrieve_download_information(self, elem):
        # return (url, filename)

        # goto download manager page
        super().get("chrome://downloads/")
        while self.execute_script("return %s" % (self._downloadManagerSelector())) is None:
            time.sleep(1)
        while self.execute_script("return %s" % (self._downloadFileSelector())) is None:
            time.sleep(1)

        # get information
        url = self.execute_script("return %s.shadowRoot.querySelector('div#content  #file-link').href" % (self._downloadFileSelector()))
        filename = self.execute_script("return %s.shadowRoot.querySelector('div#content  #file-link').text" % (self._downloadFileSelector()))

        # cancel download
        self.execute_script("%s.shadowRoot.querySelector('cr-button[focus-type=\"cancel\"]').click()" % (self._downloadFileSelector()))

        return (url, filename)

    def mark_element(self, elem_list):
        # FIXME
        return

    def _downloadManagerSelector(self):
        return "document.querySelector('downloads-manager')"

    def _downloadFileSelector(self):
        return "%s.shadowRoot.querySelector('#downloadsList downloads-item')" % (self._downloadManagerSelector())
