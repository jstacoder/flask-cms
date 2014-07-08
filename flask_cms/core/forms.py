# -*- coding: utf-8 -*-

"""
    core.forms
    ~~~~~~~~~~
"""

from flask.ext.codemirror.fields import CodeMirrorField
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField
from flask.ext.wtf import Form 
from wtforms.ext.sqlalchemy.fields import QuerySelectField,QuerySelectMultipleField
from wtforms.validators import Email, DataRequired
from wtforms import validators, fields

