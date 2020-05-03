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
from manpa_excption import InterceptionDetectedException


"""
ManpaSeleniumWebDriver is similar but not compatible with Selenium WebDriver.
You can always get the WebDriver object by .driver property.
"""


class ManpaSeleniumWebDriver(selenium.webdriver.Chrome):

    def __init__(self, parent):
        self._parent = parent
        self._parent.seleniumClientList.append(self)

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
                    "download.default_directory": self.parent._downloadDir,
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
        self._parent.seleniumClientList.remove(self)
        self._parent = None

    def get_and_wait(self, url):
        self.get(url)
        time.sleep(random.randrange(5, 10))

    def click_and_wait(self, elem):
        try:
            self.click()
            time.sleep(random.randrange(5, 10))
        except selenium.common.exceptions.ElementClickInterceptedException:
            self._parent.intercepted = True
            raise InterceptionDetectedException()

    def retrieve_download_information_and_remove_download(self):
        # return (url, filename)

        downloadManagerSelector = "document.querySelector('downloads-manager')"
        downloadFileSelector = "%s.shadowRoot.querySelector('#downloadsList downloads-item')" % (downloadManagerSelector)

        # open new tab as download manager
        self.execute_script("window.open()")
        tabs = self.get_window_handles()
        self.switch_to.window(tabs[-1])
        self.get("chrome://downloads/")
        while self.execute_script("return %s" % (downloadManagerSelector)) is None:
            time.sleep(1)
        while self.execute_script("return %s" % (downloadFileSelector)) is None:
            time.sleep(1)

        # get information
        url = self.execute_script("return %s.shadowRoot.querySelector('div#content  #file-link').href" % (downloadFileSelector))
        filename = self.execute_script("return %s.shadowRoot.querySelector('div#content  #file-link').text" % (downloadFileSelector))

        # cancel download, delete download item, close tab
        self.execute_script("%s.shadowRoot.querySelector('cr-button[focus-type=\"cancel\"]').click()" % (downloadFileSelector))
        self.close()

        return (url, filename)

    def mark_element(self, elem_list):
        # FIXME
        return
