#!/usr/bin/env python
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import shell
from papery import create_app

sh = shell.Shell(__name__)


@sh.task
def install(args):
    sh.call('pip', 'install', '-r', 'requirements.txt')
    sh.cd('theme')
    sh.call('npm', 'install', '--production')
    sh.cd('..')


@sh.task
def install_dev(args):
    sh.call('pip', 'install', '-r', 'requirements-dev.txt')
    sh.cd('theme')
    sh.call('npm', 'install', '--dev')
    sh.cd('..')


@sh.task
def rebuild_theme(args):
    sh.cd('theme')
    sh.call('npm', 'run', 'build')
    sh.cd('..')


@sh.task
def update_statics(args):
    sh.cpdir('theme/dist/js', 'papery/static/js')
    sh.cpdir('theme/dist/fonts', 'papery/static/fonts')


@sh.task
def babel_extract(args):
    sh.cd('papery')
    sh.call('pybabel', 'extract',
            '-F', 'babel.cfg',
            '-o', 'translations/messages.pot',
            '.')


@sh.task
def babel_init(args):
    sh.cd('papery')
    sh.call('pybabel', 'init',
            '-i', 'translations/messages.pot',
            '-d', 'translations',
            '-l', 'zh')


@sh.task
def babel_compile(args):
    sh.cd('papery')
    sh.call('pybabel', 'compile', '-d', 'translations')


@sh.task
def babel_update(args):
    sh.cd('papery')
    sh.call('pybabel', 'update',
            '-i', 'translations/messages.pot',
            '-d', 'translations')


@sh.task
def initdb(args):
    from papery.site.database import db
    with create_app().app_context():
        db.create_all()


@sh.task
def dropdb(args):
    from papery.site.database import db
    with create_app().app_context():
        db.drop_all()


@sh.task
def runserver(args):
    create_app().run(host='0.0.0.0')


if __name__ == '__main__':
    sh.run()
