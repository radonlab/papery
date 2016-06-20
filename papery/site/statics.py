# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from functools import partial
from flask import url_for
from .utils.avatar import url_for_avatar


def url_for_static(name):
    return url_for('static', filename=name)


def url_for_cdn(name, url_map):
    return url_map[name]


def init_app(app):
    url_map = app.config.get('CDN_URL_MAP', {})
    app.jinja_env.globals.update({
        'static': url_for_static,
        'cdn': partial(url_for_cdn, url_map=url_map),
        'avatar': url_for_avatar
    })
