# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import request
from flask.ext.babel import Babel

intl = Babel()
accept_langs = []


@intl.localeselector
def get_locale():
    return request.accept_languages.best_match(accept_langs)


def init_app(app):
    langs = app.config.get('ACCEPT_LANGUAGES', [])
    accept_langs.extend(langs)
    intl.init_app(app)
