#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

# manpa.py -
#
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

import shutil
import tempfile
import xvfbwrapper
from .manpa_util import ManpaUtil
from .manpa_selenium_client import ManpaSeleniumWebDriver


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
8. save video as log
"""


class Manpa:

    DEFAULT_WIDTH = 1280
    DEFAULT_HEIGHT = 720

    def __init__(self, width=None, height=None, downloadDir=None, videoLogFile=None, isDebug=False):
        self._width = width if width is not None else self.DEFAULT_WIDTH
        self._height = height if height is not None else self.DEFAULT_HEIGHT
        self._colordepth = 24

        if downloadDir is not None:
            self._downloadDir = downloadDir
            self._bTmpDownloadDir = False
        else:
            self._downloadDir = tempfile.mkdtemp()
            self._bTmpDownloadDir = True

        self._videoLogFile = videoLogFile
        self._isDebug = isDebug

        self._xvfb = None
        self._videoRecordProc = None
        if not self._isDebug:
            self._xvfb = xvfbwrapper.Xvfb(self._width, self._height, self._colordepth)
            self._xvfb.start()
            if self._videoLogFile is not None:
                self._videoRecordProc = ManpaUtil.createVideoRecordProcess(self._videoLogFile)

        self._httpClientList = []       # can be modified by client object
        self._seleniumClientList = []   # can be modified by client object
        self._intercepted = False       # can be modified by client object

    def dispose(self):
        self._intercepted = None
        self._seleniumClientList = None
        self._httpClientList = None
        if self._videoRecordProc is not None:
            self._videoRecordProc.terminate()
            self._videoRecordProc.wait()
            self._videoRecordProc = None
        if self._xvfb is not None:
            self._xvfb.stop()
            self._xvfb = None
        self._isDebug = None
        self._videoLogFile = None
        if self._bTmpDownloadDir:
            shutil.rmtree(self._downloadDir)
        self._bTmpDownloadDir = None
        self._downloadDir = None
        self._colordepth = None
        self._height = None
        self._width = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.dispose()

    def has_been_intercepted(self):
        return self._intercepted

    def open_http_client(self):
        return None

    def open_selenium_client(self):
        return ManpaSeleniumWebDriver(self)

    def download_files(self, url, filename):
        pass
