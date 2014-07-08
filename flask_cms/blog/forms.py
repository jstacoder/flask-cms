from flask.ext.wtf import Form,RecaptchaField
from .fields import TagField
from wtforms import StringField, validators, PasswordField, TextAreaField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from ext import db
from flask.ext.pagedown.fields import PageDownField

strip_filter = lambda x: x.strip() if x else None

#def tag_choice():
#    from blog.models import User,Category,Tag
#    return Tag.query.order_by(db.desc(Tag.name)).all()

def category_choice():
    from blog.models import Category
    return Category.query
tag_choice = category_choice

class ArticleCreateForm(Form):
    title = StringField('Title', [validators.DataRequired("Please enter a title.")],
                      filters=[strip_filter] )
    body = TextAreaField('Body', [validators.DataRequired("Please enter Somthing.")],
                         filters=[strip_filter])
    category = QuerySelectField('Category', query_factory=category_choice )
    tags = QuerySelectMultipleField('Tags',query_factory=tag_choice)
    author_name = StringField('name')
    recaptcha = RecaptchaField('are you real')
    #author_name = HiddenField()

class ArticleUpdateForm(ArticleCreateForm):
    id = HiddenField()

class CategoryCreateForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.length(min=1,max=240)])
    description = TextAreaField('Description', [validators.DataRequired()])

class TagCreateForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.length(min=1,max=240)])
    description = TextAreaField('Description', [validators.DataRequired()])

class BlogAddForm(Form):
    title = StringField('Title', [validators.DataRequired("Please enter a title.")],
                      filters=[strip_filter] )
    category = QuerySelectField('Category', query_factory=category_choice )
    #tags = QuerySelectMultipleField('Tags',query_factory=tag_choice)
    author_name = StringField('name')
    #recaptcha = RecaptchaField('are you real')
    #author_name = HiddenField()
    body = PageDownField('body')


class AddContentModalForm(Form):
    title = StringField('Title',[validators.DataRequired("Please enter a title.")])
    content = PageDownField()
    item_id = HiddenField()
    item_type = HiddenField()
    tags = TagField('Tags')
