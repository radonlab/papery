# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import subprocess
import argparse


def _execute(*args):
    """
    Execute system command.
    """
    opts = []
    for arg in args:
        if isinstance(arg, list):
            opts.extend(arg)
        else:
            opts.append(arg)
    print('Exec "%s" ...' % ' '.join(opts))
    try:
        proc = subprocess.Popen(opts,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)
        for line in proc.stdout:
            print(line.decode().rstrip())
        proc.wait()
        code = proc.returncode
    except FileNotFoundError:
        print('Unknown command "%s"' % opts[0])
        code = 2
    finally:
        if code == 0:
            print('Done.')
        else:
            print('Failed: Process exited with code %s.' % code)


class Script:
    def __init__(self):
        self.parser = argparse.ArgumentParser(__file__)
        self.subcmds = self.parser.add_subparsers(dest='subcmd')
        self.funcmap = {}

    def command(self, func):
        self.subcmds.add_parser(func.__name__)
        self.funcmap[func.__name__] = func
        return func

    def execute(self, *args):
        _execute(*args)

    def run(self):
        args = self.parser.parse_args()
        cmd = args.subcmd
        func = self.funcmap.get(cmd)
        if func:
            func()
