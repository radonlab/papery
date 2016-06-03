# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask.ext.login import LoginManager
from ..auth.models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in first.'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


def init_app(app):
    login_manager.init_app(app)
