# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext as _
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditForm(Form):
    title = StringField(_('Title'),
                        validators=[Length(0, 48, _('48 characters at most'))])
    tags = StringField(_('Tags'))
    body = TextAreaField(_('Write your article...'))
    post = SubmitField(_('Post'))
