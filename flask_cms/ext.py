# -*- coding: utf-8 -*-

"""
    ext.py
    ~~~
    :license: BSD, see LICENSE for more details
"""

from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import Form
from flask_codemirror import CodeMirror
from flask_pagedown import PageDown
#from flask.ext.script import Manager
from flask_alembic import Alembic


#manager = Manager()
pagedown = PageDown()
codemirror = CodeMirror()
alembic = Alembic()
ext = ''
# Almost any modern Flask extension has special init_app()
# method for deferred app binding. But there are a couple of
# popular extensions that no nothing about such use case.

toolbar = lambda app: DebugToolbarExtension(app)  # has no init_app()
