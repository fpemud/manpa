#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

# manpa_util.py -
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


import os
import subprocess
import fake_useragent


class ManpaUtil:

    @staticmethod
    def getRandomUserAgent(self):
        try:
            dbPath = "/usr/share/fake-useragent-db/fake_useragent_db.json"
            if os.path.exists(dbPath):
                # we don't want fake_useragent access internet
                return fake_useragent.UserAgent(path=dbPath).random
            else:
                return fake_useragent.UserAgent().random
        except fake_useragent.errors.FakeUserAgentError:
            return None

    @staticmethod
    def createVideoRecordProcess(self, width, height, colordepth, displayNumber, outputFile):
        cmd = [
            "/usr/bin/ffmpeg",
            "-f",
            "x11grab",
            "-s",
            "%dx%d" % (width, height),
            "-r",
            "%d" % (colordepth),
            "-i",
            ":%d+nomouse" % (displayNumber),
            "-c:v",
            "libx264",
            "-preset",
            "superfast",
            "-pix_fmt",
            "yuv420p",
            "-s",
            "%dx%d" % (width, height),
            "-threads",
            "0",
            "-f",
            "flv",
            outputFile,
        ]
        return subprocess.Popen(cmd)
