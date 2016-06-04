# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from .models import User
from ..site.form import Unique


class SignupForm(Form):
    email = StringField('Your Email',
                        validators=[InputRequired('Required'),
                                    Email('Invalid Email'),
                                    Unique(User,
                                           User.email,
                                           'Email is already in use')])
    username = StringField('Choose a username',
                           validators=[InputRequired('Required'),
                                       Length(1, 24, '1-24 characters'),
                                       Unique(User,
                                              User.username,
                                              'Name already exists')])
    password = PasswordField('Create a password',
                             validators=[InputRequired('Required'),
                                         Length(6, 20, '6-20 characters')])
    signup = SubmitField('Sign up')


class LoginForm(Form):
    username = StringField('Email or username',
                           validators=[InputRequired('Required')])
    password = PasswordField('Password',
                             validators=[InputRequired('Required')])
    login = SubmitField('Log in')
