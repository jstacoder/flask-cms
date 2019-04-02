from flask_wtf import Form
from wtforms import fields, validators
from wtforms.widgets.html5 import DateInput as DateWidget


class EditProfileForm(Form):
    first_name = fields.StringField('First Name')
    last_name  = fields.StringField('Last Name')
    email = fields.StringField('Email Address',validators=[validators.Required(),validators.Email()])
    phone_number = fields.StringField('phone number');
    birth_date = fields.DateField('Birth Date',format="%m-%d-%Y",validators=[validators.Optional()],widget=DateWidget())

