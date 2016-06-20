# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import Blueprint

blog = Blueprint('blog', __name__, url_prefix='/blog')

from . import views
