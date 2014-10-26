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
from flask.ext.pagedown.fields import PageDownField

class MarkdownEditor(Form):
    content = PageDownField('content')
    submit = fields.SubmitField('submit')


class TestForm(Form):
    name = fields.StringField('name')
    

class ColumnForm(Form):
    col_id = fields.HiddenField()
    column_width = fields.IntegerField('col width',description='width of columms per bootstrap3 grid')
    push = fields.IntegerField('push',description='push column x col width to the right')
    pull = fields.IntegerField('pull',description='pull column x col width to the left')
    offset = fields.IntegerField('offset',description='place column offset x col width from normal placement')



