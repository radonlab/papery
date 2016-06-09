# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from flask import render_template, request, redirect, abort, url_for, Markup
from flask.ext.login import current_user, login_required
from . import blog
from .forms import EditForm
from .models import Post, Tag
from ..auth.models import User
from ..site.database import db
from ..site.shortid import encode, decode
from ..site.utils.markdown import MarkdownRenderer


@blog.route('/')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.pub_time.desc()).paginate(page, 5)
    return render_template('blog/explore.html', posts=posts)


@blog.route('/<post_id>')
def view(post_id):
    post = Post.query.get(decode(post_id))
    if post is None:
        abort(404)
    content = Markup(MarkdownRenderer().render_text(post.body))
    return render_template('blog/view.html', content=content)


@blog.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = EditForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(form.title.data,
                    form.body.data,
                    current_user)
        for name in form.tags.data.split(','):
            name = name.strip()
            tag = Tag.query.get(name) or Tag(name)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        post_id = encode(post.id)
        return redirect(url_for('blog.view', post_id=post_id))
    return render_template('blog/edit.html', form=form)


@blog.route('/edit/<post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    return render_template('blog/edit.html')


@blog.route('/vault')
@blog.route('/vault/<post_id>')
@login_required
def vault(post_id=None):
    return render_template('blog/view.html')
