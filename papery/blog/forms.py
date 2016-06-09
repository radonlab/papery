# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditForm(Form):
    title = StringField('Title',
                        validators=[Length(0, 24, '24 characters at most')])
    tags = StringField('Tags')
    body = TextAreaField('Write your article...')
    post = SubmitField('Post')
