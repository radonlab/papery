# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

from . import views
