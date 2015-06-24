# -*- coding: utf-8 -*-

"""
    ext.py
    ~~~
    :license: BSD, see LICENSE for more details
"""
print 'imported as ',__name__

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.wtf import Form
from flask.ext.codemirror import CodeMirror
from flask.ext.pagedown import PageDown
#from flask.ext.script import Manager
from flask.ext.alembic import Alembic


#manager = Manager()
pagedown = PageDown()
codemirror = CodeMirror()
alembic = Alembic()
ext = ''
# Almost any modern Flask extension has special init_app()
# method for deferred app binding. But there are a couple of
# popular extensions that no nothing about such use case.

toolbar = lambda app: DebugToolbarExtension(app)  # has no init_app()
