#!/usr/bin/env python
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import os
import sys
import utils
from papery import create_app
from papery.site.database import db

script = utils.Script()


@script.command
def install():
    script.execute('pip', 'install', '-r', 'requirements.txt')
    os.chdir('theme')
    script.execute('npm', 'install', '--production')
    os.chdir('..')


@script.command
def install_dev():
    script.execute('pip', 'install', '-r', 'requirements-dev.txt')
    os.chdir('theme')
    script.execute('npm', 'install', '--dev')
    os.chdir('..')


@script.command
def build_theme():
    os.chdir('theme')
    script.execute('gulp', 'release')
    os.chdir('..')


@script.command
def initdb():
    with create_app().app_context():
        db.create_all()


@script.command
def dropdb():
    with create_app().app_context():
        db.drop_all()


@script.command
def runserver():
    create_app().run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    script.run()
