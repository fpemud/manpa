#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

# Copyright (c) 2019-2020 Fpemud <fpemud@sina.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
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

"""
manpa

@author: Fpemud
@license: GPLv3 License
@contact: fpemud@sina.com
"""

import os
import re
import time
import fcntl
import errno
import shutil
import fake-useragent

__author__ = "fpemud@sina.com (Fpemud)"
__version__ = "0.0.1"


"""
function list:
1. headless by xvfb, gtk-broadway, view UI any time
2. fake-useragent
3. select proxy from pool
4. control downloader
6. auto add delay
7. detect and solve interception
"""


class Manpa:

    def openHttpClient(self):
        return

    def openSeleniumClient(self):
        return



class _ManpaSeleniumClient:

    def __init__(self, downloadDir=None):
        self.downloadDir = os.getcwd() if downloadDir is None else downloadDir

        try:
            dbPath = "/usr/share/fake-useragent-db/fake_useragent_db.json"
            if os.path.exists(dbPath):
                # we don't want fake_useragent access internet
                ua = fake_useragent.UserAgent(path=dbPath).random
            else:
                ua = fake_useragent.UserAgent().random
        except fake_useragent.errors.FakeUserAgentError:
            ua = None

        options = selenium.webdriver.chrome.options.Options()
        options.add_argument('--no-sandbox')                    # FIXME
        if ua is not None:
            options.add_argument('user-agent=' + ua)
        # options.add_argument('--proxy-server=http://ip:port')
        options.add_experimental_option("prefs", {
            "download.default_directory": self.downloadDir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True,
        })
        self.driver = selenium.webdriver.Chrome(options=options)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()
        self.driver = None

    def scrollToPageEnd(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def getAndWait(self, url):
        self.driver.get(url)
        time.sleep(random.randrange(5, 10))

    def findElementByXPathAndFilterByText(self, xpath, text):
        # strange, "//a[text()='abc']" often has no effect
        for elem in self.driver.find_elements_by_xpath(xpath):
            if elem.text == text:
                return elem
        raise selenium.common.exceptions.NoSuchElementException()

    def findElementsByXPathAndFilterByText(self, xpath, text):
        # strange, "//a[text()='abc']" often has no effect
        ret = []
        for elem in self.driver.find_elements_by_xpath(xpath):
            if elem.text == text:
                ret.append(elem)
        return ret

    def clickXPathAndWait(self, xpath):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.click()
        time.sleep(random.randrange(5, 10))

    def clickElemAndWait(self, elem):
        elem.click()
        time.sleep(random.randrange(5, 10))
