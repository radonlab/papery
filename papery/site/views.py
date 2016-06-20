# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import render_template
from ..auth import auth
from ..blog import blog


def index():
    return render_template('site/index.html')


def about():
    return render_template('site/about.html')


def init_app(app):
    app.add_url_rule('/', 'site.index', index)
    app.add_url_rule('/about', 'site.about', about)
    app.register_blueprint(auth)
    app.register_blueprint(blog)
