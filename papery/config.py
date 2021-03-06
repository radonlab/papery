# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)
MASTER_EMAIL = 'letianyu@aliyun.com'

WSGI_ENV = os.environ.get('WSGI_ENV', 'production')

DEBUG = WSGI_ENV == 'development'

SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

UUID_SEQ_KEY = PROJECT_NAME + '@mserv1'

BABEL_DEFAULT_LOCALE = 'zh'
BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
ACCEPT_LANGUAGES = ['en', 'zh']

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(
    os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
    os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
    os.environ['OPENSHIFT_MYSQL_DB_HOST'],
    os.environ['OPENSHIFT_MYSQL_DB_PORT'],
    os.environ['OPENSHIFT_APP_NAME']
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

CDN_URL_MAP = {
  'jquery.min.js': '//cdn.bootcss.com/jquery/2.0.0/jquery.min.js',
  'jquery.parallax.min.js': '//cdn.bootcss.com/parallax/2.1.3/jquery.parallax.min.js'
}
