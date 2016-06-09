# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

from datetime import datetime
from ..site.database import db
from ..site.uuid import uid


post_tags = db.Table(
    'post_tags',
    db.Column('post_id',
              db.BigInteger,
              db.ForeignKey('post.id'),
              primary_key=True),
    db.Column('tag_name',
              db.String(80),
              db.ForeignKey('tag.name'),
              primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, default=uid)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mod_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    auth_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tags)

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author


class Tag(db.Model):
    name = db.Column(db.String(80), primary_key=True)

    def __init__(self, name):
        self.name = name
