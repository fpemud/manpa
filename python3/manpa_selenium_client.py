#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import time
import subprocess
import fake_useragent
from selenium import webdriver
from manpa_util import ManpaUtil


"""
ManpaSeleniumWebDriver is similar but not compatible with Selenium WebDriver.
You can always get the WebDriver object by .driver property.
"""


class ManpaSeleniumWebDriver:

    def __init__(self, downloadDir):
        self.downloadDir = downloadDir
        self.driver = None

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
        self.driver = selenium.webdriver.Chrome(options=options)

    def quit(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
        self.downloadDir = None

    def 



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
