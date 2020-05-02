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
import subprocess
import xvfbwrapper


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


class ManPa:

    def __init__(self, width=1280, height=720, videoLogFile=None):
        self.width = width
        self.height = height
        self.colordepth = 24
        self.videoLogFile = videoLogFile

        self.xvfb = xvfbwrapper.Xvfb(self.width, self.height, self.colordepth)
        self.xvfb.start()

        self.videoRecordProc = None
        if self.videoLog is not None:
            cmd = [
                "/usr/bin/ffmpeg",
                "-f",
                "x11grab",
                "-s",
                "%dx%d" % (self.width, self.height),
                "-r",
                "%d" % (self.colordepth),
                "-i",
                ":%d+nomouse" % (xvfb.vdisplay_num),
                "-c:v",
                "libx264",
                "-preset",
                "superfast",
                "-pix_fmt",
                "yuv420p",
                "-s",
                "%dx%d" % (self.width, self.height),
                "-threads",
                "0",
                "-f",
                "flv",
                self.videoLogFile
            ]
            self.videoRecordProc = subprocess.Popen(cmd)

    def dispose(self):
        if self.videoRecordProc is not None:
            self.videoRecordProc.terminate()
            self.videoRecordProc.wait()
            self.videoRecordProc = None
        if self.xvfb is not None:
            self.xvfb.stop()
            self.xvfb = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.dispose()

    def openHttpClient(self):
        return

    def openSeleniumClient(self):
        return

