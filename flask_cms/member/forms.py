from flask.ext.wtf import Form
from wtforms import fields, validators


class EditProfileForm(Form):
    first_name = fields.StringField('First Name')
    last_name  = fields.StringField('Last Name')
    email = fields.StringField('Email Address',validators=[validators.Required(),validators.Email()])
