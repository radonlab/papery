# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

SECRET_KEY = 'h8b6umefi905'

HOST_NAME = 'mserver1'

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s.db' % PROJECT_NAME
SQLALCHEMY_TRACK_MODIFICATIONS = False
