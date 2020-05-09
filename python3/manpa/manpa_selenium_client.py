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
import selenium.webdriver
from manpa.manpa_util import ManpaUtil
from manpa.manpa_exception import InterceptionDetectedException


"""
ManpaSeleniumWebDriver inherits from selenium.webdriver.Chrome.
You can always get the WebDriver object by .driver property.
"""


class ManpaSeleniumWebDriver:

    def __init__(self, parent):
        self._parent = parent
        self._parent._seleniumClientList.append(self)

        self._driver = None
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
                    "download.default_directory": self._parent._downloadDir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": False,
                    "safebrowsing.disable_download_protection": True,
                })

            # create webdriver object
            options.add_experimental_option("prefs", prefs)
            self._driver = selenium.webdriver.Chrome(options=options)
        except Exception:
            self.quit()
            raise

    def quit(self):
        if self._driver is not None:
            self._driver.quit()
            self._driver = None
        if True:
            self._parent._seleniumClientList.remove(self)
            self._parent = None

    def get_and_wait(self, url):
        self._driver.get(url)
        time.sleep(random.randrange(5, 10))

    def click_and_wait(self, elem):
        try:
            self.click(elem)
            time.sleep(random.randrange(5, 10))
        except selenium.common.exceptions.ElementClickInterceptedException:
            self._parent._intercepted = True
            raise InterceptionDetectedException()

    def retrieve_download_information_and_remove_download(self):
        # return (url, filename)
        # webdriver.find_element is not valid here because download page uses shadow DOM

        downloadManagerSelector = "document.querySelector('downloads-manager')"
        downloadFileSelector = "%s.shadowRoot.querySelector('#downloadsList downloads-item')" % (downloadManagerSelector)

        # open new tab as download manager
        self.execute_script("window.open()")
        self.switch_to.window(self.window_handles[-1])
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
        time.sleep(1)
        self.execute_script("%s.shadowRoot.querySelector('cr-icon-button[id=\"remove\"]').click()" % (downloadFileSelector))
        time.sleep(1)
        self.close()

        # return result
        return (url, filename)

    def mark_identified_element(self, element):
        # FIXME
        return

    def mark_identified_elements(self, elements):
        # FIXME
        return

    def mark_error_element(self, element, message):
        # FIXME
        return

    def mark_error_elements(self, elements, message):
        # FIXME
        return

    def __getattr__(self, attr):
        return getattr(self._driver, attr)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.quit()


class ManpaSeleniumWebElement:

    def __init__(self, elem):
        self._elem = elem

    def mark_identified(self):
        # FIXME
        return

    def mark_error(self, message):
        # FIXME
        return

    def __getattr__(self, attr):
        return getattr(self._elem, attr)
