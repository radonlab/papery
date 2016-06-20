# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import hashlib
from werkzeug.urls import url_encode

AVATAR_PROVIDER = 'www.gravatar.com'


def url_for_avatar(email, size, alter=None):
    digest = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    params = url_encode({ 's': size, 'd': alter })
    return 'http://{}/avatar/{}?{}'.format(AVATAR_PROVIDER, digest, params)
