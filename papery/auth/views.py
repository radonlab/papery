# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import render_template, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from .forms import SignupForm, LoginForm
from .models import User
from ..site.database import db


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(form.email.data,
                    form.username.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('site.index'))
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter((User.email == username) |
                                 (User.username == username)).first()
        if user is None or not user.validate(password):
            form.username.errors.append('Invalid username or password')
        else:
            login_user(user)
            return redirect(request.args.get('next') or url_for('site.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.index'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth.route('/setting')
@login_required
def setting():
    return render_template('auth/profile.html')
