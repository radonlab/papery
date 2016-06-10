# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import render_template, request, redirect, abort, url_for
from flask.ext.login import current_user, login_user, logout_user, login_required
from flask.ext.babel import gettext as _
from . import auth
from .forms import SignupForm, LoginForm
from .models import User
from ..site.database import db


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        if User.query.filter(User.email == email).first() is not None:
            form.email.errors.append(_('Email is already in use'))
        elif User.query.filter(User.username == username).first() is not None:
            form.username.errors.append(_('Name already exists'))
        else:
            user = User(email, username, password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('site.index'))
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter((User.email == username) |
                                 (User.username == username)).first()
        if user is None or not user.validate(password):
            form.password.errors.append(_('Incorrect username or password'))
        else:
            login_user(user)
            return redirect(request.args.get('next') or url_for('site.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.index'))


@auth.route('/')
@login_required
def profile():
    posts = current_user.posts
    return render_template('auth/profile.html')


@auth.route('/settings')
@login_required
def settings():
    posts = current_user.posts
    return render_template('auth/settings.html')


@auth.route('/<username>')
def view(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    return render_template('auth/view.html', user=user)
