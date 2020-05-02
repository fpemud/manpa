#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
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
    def createVideoRecordProcess(self, outputFile):
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
        return subprocess.Popen(cmd)
