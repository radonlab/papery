# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import Flask
from . import context
from . import database
from . import uuid
from . import form
from . import views

__all__ = ['create_app']


def init_app(app):
    context.init_app(app)
    database.init_app(app)
    uuid.init_app(app)
    form.init_app(app)
    views.init_app(app)


def create_app(basename):
    app = Flask(basename)
    app.config.from_pyfile('settings.py')
    init_app(app)
    return app
