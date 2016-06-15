# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, Radmon.
Use of this source code is governed by the MIT license that can be
found in the LICENSE file.
"""

import misaka as markdown
import pygments
from pygments import formatters
from pygments import lexers
from pygments.util import ClassNotFound

MARKDOWN_EXTS = ['fenced-code', 'tables']


class HighlightFormatter(formatters.HtmlFormatter):
    """
    The formatter wraps output with pre code tag.
    """
    def wrap(self, source, outfile):
        return self._wrap_pre(self._wrap_code(source))

    def _wrap_pre(self, source):
        yield 0, '<pre>'
        for tup in source:
            yield tup
        yield 0, '</pre>\n'

    def _wrap_code(self, source):
        yield 0, ('<code' + (self.cssclass and ' class="%s"' % self.cssclass)
                  + '>')
        for tup in source:
            yield tup
        yield 0, '</code>'


class ExtRenderer(markdown.HtmlRenderer):
    """
    The renderer focused on markdown code processing.
    """
    def blockcode(self, code, lang=''):
        try:
            if lang:
                lexer = lexers.get_lexer_by_name(lang)
            else:
                lexer = lexers.guess_lexer(code)
        except ClassNotFound:
            lexer = lexers.TextLexer()
        formatter = HighlightFormatter()
        return pygments.highlight(code, lexer, formatter)

    def table(self, content):
        return '<table class="table bordered">\n{}</table>\n'.format(content)


def render_text(text):
    renderer = ExtRenderer()
    parser = markdown.Markdown(renderer, extensions=MARKDOWN_EXTS)
    return parser(text)
