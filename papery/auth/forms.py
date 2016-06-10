# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext as _
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, NoneOf
from .models import User
from ..site.validators import Unique


class SignupForm(Form):
    email = StringField(_('Your Email'),
                        validators=[InputRequired(_('Required')),
                                    Email(_('Invalid Email')),
                                    Unique(User,
                                           User.email,
                                           _('Email is already in use'))])
    username = StringField(_('Choose a username'),
                           validators=[InputRequired(_('Required')),
                                       Length(1, 24, _('1-24 characters')),
                                       NoneOf(['signup',
                                               'login',
                                               'logout',
                                               'settings'],
                                              _('Unavailable')),
                                       Unique(User,
                                              User.username,
                                              _('Name already exists'))])
    password = PasswordField(_('Create a password'),
                             validators=[InputRequired(_('Required')),
                                         Length(6, 20, _('6-20 characters'))])
    signup = SubmitField(_('Sign up'))


class LoginForm(Form):
    username = StringField(_('Email or username'),
                           validators=[InputRequired(_('Required'))])
    password = PasswordField(_('Password'),
                             validators=[InputRequired(_('Required'))])
    login = SubmitField(_('Log in'))
