# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from datetime import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..site.database import db
from ..site.uuid import uid


class User(db.Model, UserMixin):
    id = db.Column(db.BigInteger, primary_key=True, default=uid)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    _password = db.Column('password', db.String(120), nullable=False)
    reg_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym('_password', descriptor=property(None, set_password))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def validate(self, password):
        return check_password_hash(self._password, password)
