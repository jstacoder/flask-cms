from flask.ext.wtf import Form,RecaptchaField
from .fields import TagField
from wtforms import StringField, validators, PasswordField, TextAreaField, HiddenField,SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from ext import db
from flask.ext.pagedown.fields import PageDownField

strip_filter = lambda x: x.strip() if x else None

#def tag_choice():
#    from blog.models import User,Category,Tag
#    return Tag.query.order_by(db.desc(Tag.name)).all()

def category_choice():
    from blog.models import Category
    return Category.query.all()
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
    tags = TagField('Tags')
    author_id = HiddenField()
    category = QuerySelectField('Category', query_factory=category_choice )
    add_cat_btn = SubmitField('Add Category')




class AddCategoryForm(Form):
    name = StringField('Name', [validators.InputRequired(), validators.length(min=1,max=240)])
    description = TextAreaField('Description', [validators.InputRequired()])
    last_url = HiddenField()

    #submit = SubmitField('Add')
    


class AddPostForm(Form):
    from blog.models import Category
    name = StringField('post name',[validators.InputRequired()])
    content = PageDownField()
    excerpt_length = StringField('excerpt Length')
    tags = TagField('tags')
    category = QuerySelectField('categoy',query_factory=category_choice)
    author = HiddenField('author_id')
    

    
