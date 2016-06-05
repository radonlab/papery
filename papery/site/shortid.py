# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import hashids

mixer = hashids.Hashids(salt='shortid salt')


def encode(value):
    return mixer.encode(value)


def decode(shortid):
    return mixer.decode(shortid)[0]


def init_app(app):
    app.jinja_env.globals.update({
        'shortid': encode
    })
