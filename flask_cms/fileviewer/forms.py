from flask_codemirror.fields import CodeMirrorField
from wtforms import fields
from flask_wtf import Form

class CodeForm(Form):
    content = CodeMirrorField('content')
    file_name = fields.HiddenField('file_name')
    submit = fields.SubmitField('submit')

