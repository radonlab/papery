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

SECRET_KEY = 'h8b6umefi905'

UUID_SEQ_KEY = PROJECT_NAME + '@mserv1'

BABEL_DEFAULT_LOCALE = 'zh'
BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
ACCEPT_LANGUAGES = ['en', 'zh']

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/papery'
else:
    import sae.const
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
        sae.const.MYSQL_USER,
        sae.const.MYSQL_PASS,
        sae.const.MYSQL_HOST,
        sae.const.MYSQL_DB)

SQLALCHEMY_TRACK_MODIFICATIONS = False

CDN_URL_MAP = {
  'jquery.min.js': '//cdn.bootcss.com/jquery/2.0.0/jquery.min.js',
  'jquery.parallax.min.js': '//cdn.bootcss.com/parallax/2.1.3/jquery.parallax.min.js'
}
