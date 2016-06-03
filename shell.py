# Copyright (C) 2015, Radmon.
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

from __future__ import absolute_import
import os
import sys
import re
import shutil
import subprocess
import collections


class LoggerError(Exception):
    u"""Indicates error raised by logger."""
    pass


class ShellError(Exception):
    u"""Indicates error raised by shell."""
    pass


class Logger(object):
    u"""Logger utility for logging with severity levels."""
    COL_GREY = 30
    COL_RED = 31
    COL_GREEN = 32
    COL_YELLOW = 33
    COL_BLUE = 34
    COL_MAGENTA = 35
    COL_CYAN = 36
    COL_WHITE = 37

    LEV_NORMAL = 0
    LEV_WARNING = 2
    LEV_ERROR = 1

    def __init__(self):
        self.colored = True
        self.level = Logger.LEV_NORMAL
        self.warning_count = 0
        self.error_count = 0

    def report(self):
        result = u'{} {}'.format(self.error_count, u'error')
        if self.error_count != 1:
            result += u's'
        if self.warning_count > 0:
            result += u', {} {}'.format(self.warning_count, u'warning')
            if self.warning_count != 1:
                result += u's'
        return result

    def _log(self, msg, *args, **kwargs):
        color = kwargs.get(u'color')
        end = kwargs.get(u'end', u'\n')
        text = msg.format(*args)
        print text,; sys.stdout.write(end)

    def trace(self, msg, *args, **kwargs):
        self._log(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(msg, *args, color=Logger.COL_BLUE, **kwargs)

    def promp(self, msg, *args, **kwargs):
        self._log(msg, *args, color=Logger.COL_GREEN, **kwargs)

    def alert(self, msg, *args, **kwargs):
        self._log(msg, *args, color=Logger.COL_MAGENTA, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(msg, *args, color=Logger.COL_YELLOW, **kwargs)
        strict = kwargs.get(u'strict', False)
        if strict:
            self.warning_count += 1
            if self.level >= Logger.LEV_WARNING:
                raise LoggerError

    def error(self, msg, *args, **kwargs):
        self._log(msg, *args, color=Logger.COL_RED, **kwargs)
        strict = kwargs.get(u'strict', False)
        if strict:
            self.error_count += 1
            if self.level >= Logger.LEV_ERROR:
                raise LoggerError


class TaskManager(object):
    u"""Utility for executing task in script."""
    def __init__(self, shell, filename):
        self.log = shell.log
        self._filename = filename
        self._task_map = collections.OrderedDict()

    def register_task(self, func, **kwargs):
        name = func.__name__
        self._task_map[name] = func

    def _get_task(self, name):
        task = self._task_map.get(name)
        if task:
            return task
        else:
            self.log.alert(u'Task "{}" not found in {}', name, self._filename)
            if self._task_map:
                msg = u', '.join(self._task_map)
                self.log.alert(u'Avaliable tasks: {}', msg)
            return None

    def _get_options(self, args):
        opts = {}
        keyword = re.compile(ur'^-[a-zA-Z][a-zA-Z0-9_]*$')
        i = 0
        while i < len(args):
            arg = args[i]
            if keyword.match(arg):
                key = arg.lstrip(u'-')
                value = True
            else:
                self.log.alert(u'Invalid argument "{}"', arg)
                break
            i += 1
            n = 1
            while i < len(args) and not keyword.match(args[i]):
                arg = args[i]
                if re.match(ur'^-?[0-9]+$', arg):
                    tmp = int(arg)
                elif re.match(ur'^-?[0-9]+\.[0-9]+$', arg):
                    tmp = float(arg)
                else:
                    tmp = arg
                if n == 1:
                    value = tmp
                elif n == 2:
                    value = [value, tmp]
                else:
                    value.append(tmp)
                n += 1
                i += 1
            opts[key] = value
        else:
            return opts
        return {}

    def parse_args(self, args):
        if len(args) > 1:
            task = self._get_task(args[1])
            opts = self._get_options(args[2:])
        else:
            task = self._get_task(u'default')
            opts = {}
        return task, opts

    def exec_task(self, task, opts):
        try:
            task(opts)
            if self.log.error_count == 0 and self.log.warning_count == 0:
                self.log.promp(u'Done, with {}.', self.log.report())
            else:
                self.log.alert(u'Done, with {}.', self.log.report())
        except ShellError:
            self.log.alert(u'Task failed.')
        except LoggerError:
            self.log.alert(u'Task failed, with {}.', self.log.report())


class Shell(object):
    u"""Common utility for shell operations."""
    def __init__(self, name):
        self.log = Logger()
        module = sys.modules.get(name)
        if hasattr(module, u'__file__'):
            path = os.path.abspath(module.__file__)
            basepath = os.path.dirname(path)
            filename = os.path.basename(path)
        else:
            basepath = os.getcwdu()
            filename = name
        self._predir = os.getcwdu()
        os.chdir(basepath)
        self._task_manager = TaskManager(self, filename)

    def pwd(self, msg=u''):
        path = os.getcwdu()
        if msg:
            self.log.info(msg, path)
        else:
            self.log.info(path)

    def cd(self, path):
        if not os.path.exists(path):
            self.log.alert(u'cd: {}: No such file or directory', path)
            raise ShellError
        if not os.path.isdir(path):
            self.log.alert(u'cd: {}: Not a directory', path)
            raise ShellError
        self._predir = os.getcwdu()
        os.chdir(path)

    def rd(self):
        self.cd(self._predir)

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        elif not os.path.isdir(path):
            self.log.alert(u'mkdir: cannot create directory "{}": '
                           u'File exists', path)
            raise ShellError

    def cp(self, src, dest):
        if os.path.isfile(src):
            shutil.copy(src, dest)
        else:
            self.log.alert(u'cp: {}: No such file', src)
            raise ShellError

    def cpdir(self, src, dest):
        if os.path.isdir(src):
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            self.log.alert(u'cpdir: {}: No such directory', src)
            raise ShellError

    def rm(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.exists(path):
            self.log.alert(u'rm: cannot remove "{}": Not a file', path)
            raise ShellError

    def rmdir(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            self.log.alert(u'rmdir: cannot remove "{}": Not a directory', path)
            raise ShellError

    def find(self, path, expr):
        pattern = re.compile(expr)
        results = []
        for root, _, files in os.walk(path):
            paths = [os.path.join(root, name) for name in files
                     if pattern.match(name)]
            results.extend(paths)
        return results

    def call(self, *args):
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, list):
                args[i:i] = args.pop(i)
        self.log.info(u'Calling "{}" ...', u' '.join(args))
        try:
            proc = subprocess.Popen(args,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    shell=True)
            for line in proc.stdout:
                self.log.trace(line.decode().rstrip())
            proc.wait()
            code = proc.returncode
        except FileNotFoundError:
            self.log.alert(u'Unknown command "{}"', args[0])
            code = 2
        finally:
            if code == 0:
                self.log.promp(u'Calling succeeded.')
            else:
                self.log.alert(u'call: errors occurred: '
                               u'Process exited with code {}.', code)
                raise ShellError

    def task(self, func=None, **kwargs):
        if callable(func):
            self._task_manager.register_task(func, **kwargs)
            return func
        else:
            def wrapper(fn):
                self._task_manager.register_task(fn, **kwargs)
                return fn
            return wrapper

    def run(self):
        task, opts = self._task_manager.parse_args(sys.argv)
        if task:
            self._task_manager.exec_task(task, opts)
