#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import time
import subprocess
import fake-useragent
from selenium import webdriver


class SeleniumClient:

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
