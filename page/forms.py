from flask.ext.codemirror.fields import CodeMirrorField
from flask.ext.wtf import Form
from wtforms import fields,validators
class EditContentForm(Form):
    content = CodeMirrorField('content')
from settings import get_choices

class ContactUsForm(Form):
    name = fields.StringField('Name',validators=[validators.DataRequired()])
    email = fields.StringField('Email',validators=[validators.DataRequired()])
    subject = fields.SelectField('Subject',validators=[validators.Optional()],choices=get_choices())
    message = fields.TextAreaField('Message',validators=[validators.DataRequired()])
