# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask.ext.wtf import csrf
from wtforms.validators import ValidationError


def init_app(app):
    csrf.CsrfProtect(app)


class Unique(object):
    def __init__(self, model, field, message='Attribute already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        obj = self.model.query.filter(field.data == self.field).first()
        if obj is not None:
            raise ValidationError(self.message)
