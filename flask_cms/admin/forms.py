from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import QuerySelectField
from wtforms import fields, validators
from ext import db
from admin.models import Type
from flask.ext.pagedown.fields import PageDownField
from flask.ext.codemirror.fields import CodeMirrorField

factory = Type.query.all()

class AddSettingForm(Form):
    name = fields.StringField('Setting Name',validators=[validators.DataRequired()])
    type = QuerySelectField('setting type',query_factory=factory,validators=[validators.DataRequired()])
    default = fields.StringField('Default Value')
    value = fields.StringField('Setting Value')

class AddSettingTypeForm(Form):
    name = fields.StringField('Setting Type Name',validators=[validators.DataRequired()])
    widget = fields.StringField('Input Widget')
    
class TestForm(Form):
    title = fields.StringField('Title')
    content = PageDownField('content')

class BaseTemplateForm(Form):
    template = fields.SelectField('base template')#,choices=[('a','a'),('b','b'),('c','c')])

class TemplateBodyFieldForm(Form):
    body = fields.TextAreaField('body')
