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


class HighlightRenderer(markdown.HtmlRenderer):
    """
    The renderer focused on markdown code processing.
    """
    def block_code(self, code, lang=None):
        try:
            if lang is None:
                lexer = lexers.guess_lexer(code)
            else:
                lexer = lexers.get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = lexers.TextLexer()
        formatter = HighlightFormatter()
        return pygments.highlight(code, lexer, formatter)


class MarkdownRenderer(object):
    """
    Markdown renderer for pygments style.
    """

    def render_text(self, string):
        """
        Render from markdown formatted string.
        """
        renderer = HighlightRenderer()
        parser = markdown.Markdown(renderer)
        return parser.parse(string)

    def render_file(self, path):
        """
        Render from markdown formatted file.
        """
        with open(path, 'r') as fp:
            text = fp.read()
        return render_text(text)
