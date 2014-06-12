from flask.ext.wtf import Form
from flask.ext.codemirror.fields import CodeMirrorField
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField,QuerySelectMultipleField
from models import Person,Category,Tag

strip_filter = lambda x: x.strip() if x else None

def category_choice():
    return Category.query.all()

def tag_choice():
    return Tag.query.all()

class ArticleCreateForm(Form):
    title = TextField('Title', [validators.Required("Please enter title.")],
                      filters=[strip_filter] )
    #body = TextAreaField('Body', [validators.Required("Please enter body.")],
    #                     filters=[strip_filter])
    body = CodeMirrorField('Markup',language="python",config={'lineNumbers':'true','matchingbracket':'true','lines':'true','cursor':'true'},validators=[validators.Required()])
    category = QuerySelectField('Category', query_factory=category_choice )
    tags = QuerySelectMultipleField('tags',query_factory=tag_choice)
    person_name = HiddenField()

class ArticleUpdateForm(ArticleCreateForm):
    id = HiddenField()

class SignupForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        person = Person.query.filter_by(email=self.email.data.lower()).first()
        if person:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = TextField("email", [validators.Required("Please enter your email")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        person = Person.query.filter_by(email=self.email.data.lower()).first()
        if person and person.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid username")
            return False

class CategoryCreateForm(Form):
    name = TextField('Name', [validators.required(), validators.length(min=1,max=240)])
    description = TextAreaField('Description', [validators.required()])

class TagCreateForm(Form):
    name = TextField('Name', [validators.required(), validators.length(min=1,max=240)])
    description = TextAreaField('Description', [validators.required()])

class PersonUpdateForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
