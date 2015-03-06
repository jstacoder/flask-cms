from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import fields, validators,widgets
from wtforms.widgets.core import Option
#from admin.models import Type
from .fields import TagField
from flask.ext.pagedown.fields import PageDownField
from flask.ext.codemirror.fields import CodeMirrorField
from page.fields import CKTextEditorField
#from blog.models import Category
from wtforms.widgets.html5 import DateInput as DateWidget
#from icons import el_icon as icons
import admin.icons as admin_icons
#from .fields import AceEditorField
from flask import Markup
from settings import BaseConfig


from page.utils import get_page_templates

lib = BaseConfig.DEFAULT_ICON_LIBRARY
icons = __import__('admin.icons',[],[],'icons').__dict__[lib]
icon_fmt = '<i class="{1} {1}-{0}"></i>'
icon_choices = {str(x):icon_fmt.format(x,lib) for x in icons}

#icons = [(icon_format.format(x,lib),x) for x,lib in icon_libs.items()]

#factory = Type.query.all()

class AddSettingForm(Form):
    name = fields.StringField('Setting Name',validators=[validators.InputRequired()])
    #type = QuerySelectField('setting type',query_factory=factory,validators=[validators.InputRequired()])
    default = fields.StringField('Default Value')
    value = fields.StringField('Setting Value')

class AddSettingTypeForm(Form):
    name = fields.StringField('Setting Type Name',validators=[validators.InputRequired()])
    widget = fields.StringField('Input Widget')

class TestForm(Form):
    title = fields.StringField('Test')
    #content = AceEditorField('content')
    submit = fields.SubmitField()

class BaseTemplateForm(Form):
    template = fields.SelectField('base template',validators=[validators.InputRequired()])#,choices=[('a','a'),('b','b'),('c','c')])

class TemplateBodyFieldForm(Form):
    name = fields.HiddenField()
    body = CKTextEditorField('body')

class TextEditorFieldForm(Form):
    content = CKTextEditorField('content')
    
class TextEditorContentForm(Form):
    content = fields.FormField(TextEditorFieldForm,label="Content",separator="_")
    submit = fields.SubmitField('save')

AddTemplateForm = TemplateBodyFieldForm

def cat_factory():
    from blog.models import Category
    return Category.query.all()

class AddBlogForm(Form):
    name = fields.StringField('Blog Name',validators=[validators.InputRequired()])
    title = fields.StringField('Blog Title',validators=[validators.InputRequired()])
    slug = fields.StringField('Url Slug')
    category = QuerySelectField('category',query_factory=cat_factory)
    author_id = fields.HiddenField()
    date_added = fields.HiddenField()

class AddMacroForm(Form):
    name = fields.StringField('Macro Name',validators=[validators.InputRequired()])
    content = CKTextEditorField('Body')
    arg = fields.StringField('argument')
    default = fields.StringField('arg default')
    


class AddPageForm(Form):
    date_added = fields.DateField('Publish On:',format="%m-%d-%Y",widget=DateWidget())
    date_end = fields.DateField('Expire On:',format="%m-%d-%Y",validators=[validators.Optional()],widget=DateWidget())
    name = fields.StringField('Page Name',validators=[validators.InputRequired()])
    description = fields.TextAreaField('Description',validators=[validators.Optional()])
    slug = fields.StringField('Page Slug',validators=[validators.InputRequired()])
    short_url = fields.StringField('Url',validators=[validators.Optional()])
    title = fields.StringField('Page Title',validators=[validators.InputRequired()])
    add_to_nav = fields.BooleanField('Add to Navbar')
    add_sidebar = fields.BooleanField('Add Sidebar')
    visible = fields.SelectField(choices=((1,'Publish'),(0,'Draft')))
    meta_title = fields.StringField('Meta Title',validators=[validators.InputRequired()])
    content = CodeMirrorField('Content',language='xml',config={'lineNumbers':'true'})
    template = fields.FormField(BaseTemplateForm,label="Template",separator='_')
    blocks = fields.SelectMultipleField(label="blocks",choices=[('a','a'),('b','b'),('c','c')])
    category = QuerySelectField('category')
    tags = TagField('Tags')
    use_base_template = fields.BooleanField('Use Base Template')
    base_template =  fields.SelectField(
                        'base template',validators=[
                            validators.InputRequired()
                        ],choices=[
                            (x,x) for x in sorted(get_page_templates()) \
                            if not x.startswith('_') and not \
                            x.startswith('.') and x.endswith('.html')
                        ]
    )
    submit = fields.SubmitField('Save')


class AddButtonForm(Form):
    name = fields.StringField('button id',validators=[validators.InputRequired()])
    size = fields.SelectField('button size',choices=(
                                        ('xs','x-sm'),('s','small'),
                                        ('m','med'),('l','lrg'),('xl','x-lg')
                                        ))
    color = fields.SelectField('Button color',choices=(
                                        ('blue','blue'),('red','red'),('grey','grey'),
                                        ('green','green'),('yellow','yellow'),('light-blue','light-blue')
                                        ))
    text = fields.StringField('Button text',validators=[validators.InputRequired()])
    icon = fields.SelectField('Button icon',choices=icon_choices.items())
    icon_library = fields.HiddenField('icon_library')
    type = fields.RadioField('Button type',choices=(('submit','submit'),('button','button'),('link','link')))
    link_href = fields.StringField('link url, can be endpoint or uri')



class AddStaticBlockForm(Form):
    name = fields.StringField('Block Name',validators=[validators.InputRequired()])
    block_id = fields.StringField('Block Identifer(for templates)',validators=[validators.InputRequired()])
    content = CKTextEditorField('content')

class AddAdminTabForm(Form):
    name = fields.StringField('Tab Name',description='displayed on tab',validators=[validators.InputRequired()])
    tab_id = fields.StringField('tab identifer',description='for calling in templates',validators=[validators.InputRequired()])
    tab_title = fields.StringField('tab title',description='title on tabbed on content',validators=[validators.InputRequired()])
    content = fields.TextAreaField()#CKTextEditorField()


class AdminEditFileForm(Form):
    content = CKTextEditorField('content')
    file_name = fields.HiddenField()



class TemplateWizardRowCountForm(Form):
    row_count = fields.RadioField('row count',choices=((1,1),(2,2),(3,3)),validators=[validators.InputRequired()])



class TemplateWizardSingleRowForm(Form):
    row_height = fields.IntegerField('row height',default='100')
    column_count = fields.RadioField('Row columns',choices=((1,1),(2,2),(3,3),(4,4),(5,5)))
    row_count = fields.HiddenField()
    current_row = fields.HiddenField()

class TemplateWizardSingleColumnForm(Form):
    block_name = fields.StringField('block name',validators=[validators.InputRequired()])
    column_width = fields.IntegerField('Column Width',description='per bootstrap grid',validators=[validators.InputRequired()])


class HeightFields(Form):
    height_a = fields.IntegerField('height a')
    height_b = fields.IntegerField('height b')
    height_c = fields.IntegerField('height c')


class ColumnFields(Form):
    left_bar  = fields.IntegerField()
    col_1 = fields.IntegerField()
    col_2 = fields.IntegerField()
    col_3 = fields.IntegerField()
    right_bar = fields.IntegerField()


class CreateGridForm(Form):
    row_count = fields.RadioField('row count',choices=((1,1),(2,2),(3,3)),validators=[validators.InputRequired()])
    row_heights = fields.FormField(HeightFields)
