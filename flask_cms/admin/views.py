# -*- coding: utf-8 -*-

"""
    admin.views

    Administrative Views
"""
import os
from .utils import login_required
from datetime import datetime
from flask.ext.wtf import Form
from wtforms.fields import FormField,SelectField
from wtforms.ext.sqlalchemy.orm import model_form
#from wtalchemy.orm import model_form
from flask.ext.xxl.baseviews import BaseView,ModelView
from admin import admin
from flask import request,session,flash,jsonify
from .forms import (
        AddBlogForm, AddButtonForm,
        TextEditorFieldForm,AddMacroForm,
        TextEditorContentForm,AddAdminTabForm,
        AdminEditFileForm
)
from .utils import get_files_of_type
from ext import db
from settings import BaseConfig

root = BaseConfig.ROOT_PATH

class FakePage(object):
    link = None
    text = None

    def __init__(self):#,page):
        self.text = ''#page.title
        self.link = ''#page._get_page_url()

    def test_method(self):
        return True

class AdminDashboardView(BaseView):
    _template = 'dashboard.html'

    decorators = [login_required]

    def get(self):

        return self.render()

class AdminSiteSettingsView(BaseView):
    _template = 'settings.html'

    decorators = [login_required]

    def get(self):
        '''from admin.forms import SiteSettingsForm
        from admin.models import SiteSetting
        settings = SiteSettings.query.all()
        self._form = SiteSettingsForm(obj=settings)'''
        return self.render()



class AdminPageView(BaseView):
    _template = 'add.html'
    _context = {
                    'form_args':
            {
                'heading':'Add CMS Page',
            }
    }

    decorators = [login_required]

    def get(self):
        if not 'content' in request.endpoint:
            from page.models import Page
            from wtforms import FormField
            from admin.forms import BaseTemplateForm
            from auth.models import User
            from page.models import Template
            self._context['choices'] = [(x,x.name) for x in Template.query.all()]
            from ext import db
            form = model_form(Page,db.session,base_class=Form,exclude=['date_added','added_by'])
            class PageForm(form):
                template = FormField(BaseTemplateForm)
                def __init__(self,*args,**kwargs):
                    if 'prefix' in kwargs:
                        kwargs.pop('prefix')
                    super(PageForm,self).__init__(*args,**kwargs)

            self._form = PageForm(prefix=False)
        else:
            from page.forms import EditContentForm
            from auth.models import User
            self._form = EditContentForm
        return self.render()

    def post(self):
        if 'content' in request.endpoint:
            session['content'] = request.form['content'][:]
            return self.redirect('admin.add_page')
        else:
            from auth.models import User
            from admin.forms import BaseTemplateForm
            from page.models import Template
            from page.models import Page
            from wtforms import FormField
            from ext import db
            self._context['choices'] = [(x,x.name) for x in Template.query.all()]
            form = model_form(Page,db.session,base_class=Form,exclude=['date_added','added_by'])
            class PageForm(form):
                template = FormField(BaseTemplateForm)

                def _get_template_id(self,template_name):
                    from page.models import Template
                    t = Template.query.filter(Template.name==template_name).first()
                    if t:
                        return t.id
                    return None

                def __init__(self,*args,**kwargs):
                    if 'prefix' in kwargs:
                        kwargs.pop('prefix')
                    super(PageForm,self).__init__(*args,**kwargs)
                def populate_obj(self,obj):
                    for name,field in self._fields.items():
                        if name == 'template':
                            obj.template_id = self._get_template_id(field.template.data)
                            self._fields.pop(name)
                    super(PageForm,self).populate_obj(obj)

            self._form = PageForm(request.form)
            page = Page()
            self._form.populate_obj(page)
            if 'content' in session:
                page.content = session.pop('content',None)
            page.save()
            flash('Successfully created cms page: {}'.format(page.name))
            return self.redirect('admin.pages')
        return self.render()


def switch(x):
    return x[1],x[0]

def fix_choices(choices):
    return map(switch,choices)

class AdminTemplateAjaxView(BaseView):
    def get(self):
        result = {'result':'error','content':''}
        filename = request.args.get('filename',None)
        if filename is not None:
            filename = os.path.join(root,'templates',filename)
            if os.path.exists(filename):
                with open(filename,'r') as fp:
                    result['result'] = 'success'
                    result['content'] = fp.read()
        return jsonify(result)

class AdminTemplateView(BaseView):
    _template = 'add.html'
    _context = {'use_ck':False,
                    'form_args':
            {
                'heading':'Add a Template',
            }
    }

    decorators = [login_required]

    def get(self):
        from auth.models import User
        from page.models import Template
        from wtforms import FormField
        from admin.forms import TemplateBodyFieldForm
        from ext import db
        from settings import BaseConfig
        AddTemplateForm = model_form(Template,db.session,base_class=Form,exclude=['blocks','pages','body','base_template'])
        class TemplateForm(AddTemplateForm):
            body = FormField(TemplateBodyFieldForm)
            base_template = SelectField('Base Template',choices=fix_choices(BaseConfig.BASE_TEMPLATE_FILES))

        self._form = TemplateForm
        return self.render()

    def post(self):
        from page.models import Template
        from auth.models import User
        from ext import db
        self._form = model_form(Template,db.session,base_class=Form,exclude=['blocks','pages','body'])(request.form)
        if self._form.validate():
            template = Template()
            self._form.populate_obj(template)
            template.save()
            filename = template.filename
            if template.body is not None:
                body = template.body[:]
            else:
                body = ''
            from settings import BaseConfig
            import os
            templatedir = os.path.join(BaseConfig.ROOT_PATH,'templates')
            os.system('touch {}'.format(os.path.join(templatedir,filename)))
            fp = open(os.path.join(templatedir,filename),'w')
            fp.write(body+'\n')
            fp.close()
            flash('you have created a new template named: {}'.format(template.name))
            return self.redirect('admin.templates')
        else:
            flash('You need to give the template a name')
        return self.render()

    @staticmethod
    @admin.before_app_request
    def check_templates():
        from page.models import Template
        from auth.models import User
        from app import app
        from blog.models import Article
        templates = Template.query.all()
        template_dir = app.config['ROOT_PATH'] + '/' + 'templates'
        if not os.path.exists(template_dir):
            os.mkdir(template_dir)
        names = [t.name for t in templates]
        for t in os.listdir(template_dir):
            if not t in names:
                temp = Template()
                temp.name = t
                temp.filename = os.path.join(template_dir,t)
                temp.body = open(os.path.join(template_dir,t),'r').read()
                temp.save()

class AdminBlockView(BaseView):
    _template = 'add.html'
    _context = {'mce':True,
                    'form_args':
            {
                'heading':'Add CMS Block',
            }
    }

    decorators = [login_required]

    def get(self):
        if not 'content' in request.endpoint:
            from auth.models import User
            from page.models import Block
            from ext import db
            AddBlockForm = model_form(Block,db.session,base_class=Form)
            self._form = AddBlockForm
        else:
            content = session.pop('content','')
            from page.forms import EditContentForm
            self._form = EditContentForm
            self._form.content.data = content
        return self.render()

    def post(self):
        if 'content' in request.endpoint:
            session['content'] = request.form['content'][:]
            return self.redirect('admin.add_block')
        else:
            content = session.pop('content',None)
            from page.models import Block
            from ext import db
            AddBlockForm = model_form(Block,db.session,base_class=Form)
            self._form = AddBlockForm(request.form)
            block = Block()
            self._form.populate_obj(block)
            if 'content' in session:
                block.content = content
            block.save()
            flash('Successfully created cms block: {}'.format(block.name))
            return self.redirect('admin.blocks')
        return self.render()
    @staticmethod
    @admin.before_app_request
    def check_blocks():
        from page.models import Block as model
        from auth.models import User
        objs = model.query.all()
        from app import app
        block_dir = app.config['ROOT_PATH'] + '/' + 'blocks'
        if not os.path.exists(block_dir):
            os.mkdir(block_dir)
        names = [o.name for o in objs]
        for o in os.listdir(block_dir):
            if not o in names:
                if not o.startswith('_'):
                    temp = model()
                    temp.name = o
                    temp.content = ''.join(map(str,open(os.path.join(block_dir,o),'r').readlines()))
                    temp.save()

class AdminCMSListView(BaseView):
    _template = 'list.html'
    _context = {}

    decorators = [login_required]

    def get(self):
        from settings import BaseConfig
        pp = BaseConfig.ADMIN_PER_PAGE
        Button = None
        if 'buttons' in request.endpoint:
            from page.models import Button
            obj = Button
            self._template = 'show_buttons.html'
        if 'users' in request.endpoint:
            from auth.models import User
            obj = User
        if 'page' in request.endpoint:
            from page.models import Page
            obj = Page
        if 'block' in request.endpoint:
            from page.models import Block
            obj = Block
        if 'blog' in request.endpoint:
            from blog.models import Blog
            obj = Blog
        if 'template' in request.endpoint:
            from page.models import Template
            obj = Template
        objs = obj.query.all()
        if len(objs) > pp and not Button:
            return self.redirect('admin.page_{}'.format(obj.__name__.lower()),page_num=1)
        exclude = ['password','templates','pages','id','body','content',
                    'query','metadata','template','blocks','body_body',
                    'template_id','use_base_template','absolute_url','body-body',
                    'added_by','body_body','articles','role_id','_pw_hash',
                    'is_unknown','posts','author_id','category_id',]
        headings = obj.get_all_columns(exclude)
        self._context['objs'] = objs
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        return self.render()


class AdminListPageView(BaseView):
    _template = 'list.html'

    decorators = [login_required]

    def get(self,page_num=1):
        from admin.utils import Pagination
        from settings import BaseConfig
        pp = BaseConfig.ADMIN_PER_PAGE
        endpoint = request.endpoint
        if '_users' in endpoint:
            from auth.models import User
        if '_page' in endpoint:
            from page.models import Page as model
        elif '_template' in endpoint:
            from page.models import Template as model
        else:
            from page.models import Block as model
        p = Pagination(model,page_num)
        self._context['objs'] = p._objs
        self._context['pagination'] = p
        exclude = ['password','templates','pages','id','body','content',
                    'query','metadata','template','blocks','body-body',
                    'template_id','use_base_template','absolute_url','body_body',
                    'added_by','articles','role_id','_pw_hash','is_unknown']
        headings = p._objs[0].get_all_columns(exclude)
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        self._context['use_codemirror'] = True
        
        return self.render()

class AdminListedView(BaseView):
    _template = 'list_blogs.html'
    
    def get(self):
        self._context['add_sidebar'] = True
        self._context['excludes'] =\
                    ['password','templates','pages','id','body','content',
                    'query','metadata','template','blocks','body-body',
                    'template_id','use_base_template','absolute_url','body_body',
                    'added_by','articles','role_id','_pw_hash','is_unknown','macros',
                    'description','posts','user_id','blogs','_args','args']
        self._context['obj_list'] = [['blog'],['page'],['user','auth'],['macro','page'],['template','page']]
        return self.render()
        
class AdminModalView(BaseView):
    _template = 'modal.html'
    def get(self):
        return self.render()
    


class AdminDetailView(BaseView):

    decorators = [login_required]

    def get(self,slug=None,name=None):
        endpoint = request.endpoint[:]
        if 'page' in request.endpoint:
            self._template = 'view_page.html'
        if 'block' in request.endpoint:
            self._template = 'view_block.html'
        if 'template' in request.endpoint:
            self._template = 'view_template.html'
        if 'page' in endpoint:
            from page.models import Page
            obj = Page.query.filter(Page.slug==slug).first()
        if 'block' in endpoint:
            from page.models import Block
            obj = Block.query.filter(Block.name==name).first()
        if 'template' in endpoint:
            from page.models import Template
            obj = Template.query.filter(Template.name==name).first()

        self._context['obj'] = obj
        self._context['lines'] = obj.content.split('\n') or obj.body.split('\n')
        return self.render()



class AdminEditView(BaseView):
    _template = 'add.html'
    _context = {
                    'form_args':
            {
                'heading':'Edit CMS Item',
            }
    }

    decorators = [login_required]

    def get(self,item_id=None):
        from auth.models import User
        from ext import db
        if 'page' in request.endpoint:
            from page.models import Page
            page = Page.get_by_id(item_id)
            if not 'content' in request.endpoint:
                self._form = model_form(Page,db.session,base_class=Form,exclude=['added_by','date_added'])
                self._context['obj'] = page
            else:
                from page.forms import EditContentForm
                self._form = EditContentForm
            self._form_obj = page
        elif 'block' in request.endpoint:
            from page.models import Block
            block = Block.get_by_id(item_id)
            if not 'content' in request.endpoint:
                self._form = model_form(Block,db.session,base_class=Form,exclude=['templates','pages'])
                self._context['obj'] = block
            else:
                from page.forms import EditContentForm
                self._form = EditContentForm
            self._form_obj = block
        else:
            from admin.forms import TemplateBodyFieldForm
            from wtforms import FormField
            from page.models import Template
            template = Template.get_by_id(item_id)
            form = model_form(Template,db.session,base_class=Form,exclude=['pages','blocks','filename','body'])

            class TemplateForm(form):
                body = FormField(TemplateBodyFieldForm,separator='_')
            self._form = TemplateForm
            self._context['obj'] = template
            self._form_obj = template
        return self.render()

    def post(self,item_id=None):
        from ext import db
        from auth.models import User
        if 'content' in request.endpoint:
            session['content'] = request.form['content'][:]
            return self.redirect('admin.edit_{}'.format(request.url.split('/')[-3]),item_id='{}'.format(request.url.split('/')[-1]))
        else:
            if 'page' in request.endpoint:
                from page.models import Page as model
                needs_content = True
                msg = 'cms page'
                redirect = 'pages'
                exclude = ['added_by','date_added']
            if 'block' in request.endpoint:
                from page.models import Block as model
                needs_content = True
                msg = 'cms block'
                redirect = 'blocks'
                exclude = ['templates','pages']
            if 'template' in request.endpoint:
                from page.models import Template as model
                needs_content = False
                msg = 'template'
                redirect = 'templates'
                exclude = ['pages','blocks']
            self._form = model_form(model,db.session,base_class=Form,exclude=exclude)(request.form)
            obj = model.query.filter(model.id==item_id).first()
            self._form.populate_obj(obj)
            if needs_content:
                if 'content' in session:
                    obj.content = session.pop('content',None)
            obj.update()
            flash('Successfully updated {}: {}'.format(msg,obj.name))
            return self.redirect('admin.{}'.format(redirect))

class TestView(BaseView):
    _template = 'add.html'
    _form = None
    _context = {}

    def get(self):
        from admin.forms import TestForm
        self._form = TestForm
        self._form._has_pagedown = False
        self._context['url_link'] = 'admin.test'
        return self.render()



class PageListView(BaseView):
    _template = 'list_pages.html'
    _context = {}

    def get(self):
        from page.models import Page
        pages = [FakePage(page) for page in Page.query.all()]
        self._context['page_list'] = pages
        return self.render()


class AdminSettingsView(BaseView):
    _template = 'settings.html'
    _form = None # uses AddSettingForm and SettingForm
    _context = {}

    def get(self):
        self._get_settings_widgets()
        return self.render()

    def _get_settings_widgets(self):
        from .models import Setting
        self._context['widgets'] = [x.widget for x in Setting.query.all()]


class AdminAddCategoryView(BaseView):
    from blog.forms import AddCategoryForm
    _template = 'add.html'
    _form = AddCategoryForm
    _context = {}
    _form_heading = 'Add a Category'
   
    decorators = [login_required]

    def get(self):
        self._context['form_args'] = {'heading':self._form_heading}
        return self.render()

    def post(self):
        self._context['form_args'] = {'heading':self._form_heading}
        self._form = self._form(request.form)
        if self._form.validate():
            from blog.models import Category
            c = Category.query.filter(Category.name==self._form.name.data).first()
            if c is None:
                c = Category()
                c.name = self._form.name.data
                c.description = self._form.description.data
                c.save()
                self.flash('You added category: {}'.format(c.name))
                if request.args.get('last_url'):
                    return self.redirect(request.args.get('last_url'),raw=True)
            else:
                self.flash('There is already a category by that name, try again')
        return self.redirect('core.index')

class AdminBlogView(BaseView):
    _template = 'blog_settings.html'
    _form = None
    _context = {}

    def get(self,blog_id=None):
        return self.render()

class AdminAddBlogView(BaseView):
    _template = 'add.html'
    _form = None
    _context = {}

    decorators = [login_required]

    def get(self):
        self._form = AddBlogForm(author_id=session.get('user_id'),date_added=datetime.now())
        return self.render()

    def post(self):
        self._form = AddBlogForm(request.form)
        if self._form.validate():
            from blog.models import Blog
            blog = Blog()
            blog.name = self._form.name.data
            blog.date_added = self._form.date_added.data
            blog.title = self._form.title.data
            blog.slug = self._form.slug.data
            author_id = self._form.author_id.data
            category = self._form.category.data
            blog.save()
        return self.redirect('blog.list')





    
#from flask import jsonify
#@admin.route('/add/tst')
#def tst():
#    num = request.args.get('num',None)
#    if num is None:
#        res = {'val':'none'}
#    else:
#        res = {'num':num*2}
#    return jsonify(result=res)



class AdminAddButtonView(BaseView):
    _template = 'add.html'
    _form = AddButtonForm
    _context = {}

    def get(self):
        self._form = AddButtonForm(icon_library=BaseConfig.DEFAULT_ICON_LIBRARY)
        return self.render()

    def post(self):
        from page.models import Button
        if self._form().validate():
            f = self._form()
            b = Button.query.get(Button.get_id_by_name(f.name.data))
            if b is not None:
                self.flash('There is already a button by that name')
            else:
                b = Button()
                b.name = f.name.data
                b.size = f.size.data
                b.color = f.color.data
                b.text = f.text.data
                b.icon = f.icon.data
                b.icon_library = f.icon_library.data
                b.type = f.type.data
                if b.type == 'link':
                    b.is_link = True
                    b.endpoint = f.link_href.data
                else:
                    b.is_link = False
                b.save()
                return self.redirect('admin.view_button',item_id=b.id)
            return self.render()
        return self.render()

class AdminShowButtonView(BaseView):
    _template = 'show.html'
    _context = {}

    def get(self,item_id):
        from page.models import Button
        self._context['button'] = Button.get_by_id(item_id).name
        return self.render()

class AdminStaticBlockView(BaseView):
    _template = 'add_block.html'
    _context = {'use_ck':True,
                'remove_jquery':True}                  

    def get(self,item_id=None):
        from page.models import StaticBlock
        from .forms import AddStaticBlockForm
        form = AddStaticBlockForm #model_form(StaticBlock,db.session,base_class=Form,exclude=['content'])
        if 'list' in request.endpoint:
            self._template = 'sort_list.html'
            self._context['list_items'] = StaticBlock.query.all() or []
        elif 'add' in request.endpoint:            
            class StaticBlockForm(form):
                content = FormField(TextEditorFieldForm,'_')
            self._form = form #StaticBlockForm
        elif 'edit' in request.endpoint:
            self._template = 'add_block.html'
            class StaticBlockForm(form):
                content = FormField(TextEditorFieldForm,'_')
            self._form = form # form StaticBlockForm
            self._form_obj = StaticBlock.get_by_id(item_id)
            self._context['content'] = self._form_obj.content[:]
            self._context['obj'] = self._form_obj
        return self.render()
    
    def post(self,item_id=None):
        from page.models import StaticBlock
        form = model_form(StaticBlock,db.session,base_class=Form,exclude=['content'])
        class StaticBlockForm(form):
            content = FormField(TextEditorFieldForm,'_')
        self._form = StaticBlockForm
        if item_id is None:
            block = StaticBlock()
            msg = "created a new"
        else:
            block = StaticBlock.get_by_id(item_id)
            msg = "updated a"
        data = self.get_form_data()
        block.name = data['name']
        block.content = data['content']['content']
        block.block_id = data['block_id']
        if block.save():
            flash(msg + " static_block with id: {}".format(block.block_id))
            return self.redirect('admin.index')
        else:
            flash("Error")
        return self.render()


class AdminAddMacroView(BaseView):
    _template = 'add.html'
    _context = {}
    _form = AddMacroForm

    def get(self):
        return self.render()

class AdminCodeView(BaseView):
    _template = 'code.html'
    _context = {}
    
    def get(self,file_path=None):
        py_files_by_dir,count_list = get_files_of_type('.py')
        if file_path is None:
            self._context['dir_list'] = [x.split('/')[-1] for x in py_files_by_dir.keys()]
            self._context['dir_dict'] = {x.split('/')[-1]:y for x,y in py_files_by_dir.items()}
            self._context['file_counts'] = count_list
        else:
            self._context['file'] = py_files[file_path]
        return self.render()


class AdminBlogListView(BaseView):
    _template = 'list_blogs.html'
    _context = {}

    def get(self):
        exclude = [
                    'password','templates','pages','id','body','content',
                    'query','metadata','template','blocks','body-body',
                    'template_id','use_base_template','absolute_url','body_body',
                    'added_by','articles','role_id','_pw_hash','is_unknown',
                    'posts','author_id','category_id',
                    ]
        from blog.models import Blog
        self._context['blogs'] = Blog.query.all()
        headings = Blog.get_all_columns(exclude)
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        self._context['add_sidebar'] = True                
        return self.render()



class AdminTabView(BaseView):
    _template = 'add.html'
    _context = {'use_ck':True}
    _form = AddAdminTabForm

    def get(self):
        if 'add' in request.endpoint:
            return self.render()        
        else:
            from .models import AdminTab
            name = request.args.get('name',None)
            at = AdminTab.query.filter(AdminTab.name==name).first()
            if at is not None:
                self.flash('that names already taken, must be popular')
                return jsonify({'error':True})
            else:
                at = AdminTab()
                at.name = name
                at.tab_id = request.args.get('tab_id',None)
                at.tab_title = request.args.get('tab_title',None)
                at.content = request.args.get('content',None)
                at.save()
                return jsonify({'success':True})


class AdminFilesystemView(BaseView):
    _template = 'filesystem.html'
    _context = {}

    def get(self):
        dirName = request.args.get('dirName',None)
        fileName = request.args.get('fileName',None)
        if fileName is None:
            # serve the given dir
            if dirName is None:
                # serve from base dir
                dirName = os.getcwd()
            self._context['fileList'] = self.get_file_list(dirName)
            self._context['parent'] = os.path.abspath(os.path.join(os.pardir,dirName))
            self._context['dirList'] = self.get_file_list(dirName,files=False)
            self._context['dirName'] = os.path.join(root,dirName)
            if not len(self._context['dirList']) == len(self._context['fileList']):
                if len(self._context['dirList']) > len(self._context['fileList']):
                    diff = len(self._context['dirList']) - len(self._context['fileList'])
                    self._context['fileList'] = self._context['fileList'] + [None]*diff
                else:
                    diff = len(self._context['fileList']) - len(self._context['dirList'])
                    self._context['dirList'] = self._context['dirList'] + [None]*diff
        else:
            self._template = 'edit_file.html'
            self._context['file'] = os.path.join(os.path.join(root,dirName),fileName)
            self._context['content'] = open(self._context['file'],'r').read() or ' '
            self._context['use_ck'] = True
            self._context['editor_mode'] = 'python'
            self._form = AdminEditFileForm(file_name=self._context['file'],
                                                content=self._context['content'])
        return self.render()
    
    def get_file_list(self,dirName=None,files=True):
        import os
        if files:
            func = self.filter_files
        else:
            func = self.filter_dirs
        if dirName is None:
            dirName = os.getcwd()
        dirName = os.path.join(root,dirName)
        return sorted(func(os.listdir(dirName)))

    def filter_files(self,files):
        return [f for f in files if not f.endswith('.pyc') and not os.path.isdir(f)]
    
    def filter_dirs(self,files):
        return [str(d) for d in files if os.path.isdir(os.path.join(root,d))]
       
        


class IconView(BaseView):
    _template = 'show_icons.html'

    def get(self,lib=None):
        #from .icons import icons
        if lib is None:
            if request.endpoint == 'admin.all_icons':
                import admin.icons as ai
                self._context['libs'] = {
                    str(x) : __import__(
                                'admin.icons',[],[],'icons'
                    ).__dict__[x] for x in dir(ai) if not x.startswith('_')
                }
        else:
            icons = __import__('admin.icons',[],[],'icons').__dict__[lib]
            lib = IconView._fix_lib_name(lib)
            self._context = {
                'lib':lib,
                'icons':icons,
            }
        return self.render()

    @staticmethod
    def _fix_lib_name(name):
        tmp = name.split('_')
        if len(tmp) > 1:
            name = '-'.join(map(str,tmp))
        return name
