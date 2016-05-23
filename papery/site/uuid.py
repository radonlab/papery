# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import time
import datetime
import random
import hashlib


class UUID64(object):
    def __init__(self):
        self._epoch = 0
        self._number = 0

    def set_epoch(self, date):
        assert self._epoch == 0
        sec = time.mktime(date.timetuple())
        self._epoch = int(sec * 1000)

    def set_seq_number(self, num):
        assert self._number == 0
        self._number = num & 0x3ff

    def set_seq_name(self, name):
        digest = hashlib.sha1(name.encode('utf-8')).hexdigest()
        self.set_seq_number(int(digest, 16))

    def generate(self):
        msec = int(time.time() * 1000) - self._epoch
        high = msec & 0x1ffffffffff
        low = random.getrandbits(12)
        return high << 22 | self._number << 12 | low

    def __call__(self):
        return self.generate()


uid = UUID64()


def init_app(app):
    uid.set_epoch(datetime.date(2010, 1, 1))
    uid.set_seq_name(app.config.get('HOST_NAME', ''))
