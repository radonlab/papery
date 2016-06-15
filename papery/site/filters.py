# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from .utils.markdown import render_text


def init_app(app):
    app.jinja_env.filters.update({
        'markdown': render_text
    })
