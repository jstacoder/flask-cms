# -*- coding: utf-8 -*-

"""
    admin.views

    Administrative Views
"""
import os
from auth.utils import login_required
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from baseviews import BaseView,ModelView
from admin import admin
from flask import request,session,flash

class FakePage(object):
    link = None
    text = None

    def __init__(self,page):
        self.text = page.title
        self.link = page._get_page_url()

class AdminDashboardView(BaseView):
    _template = 'dashboard.html'

    decorators = [login_required]

    def get(self):
        
        return self.render()

admin.add_url_rule('', view_func=AdminDashboardView.as_view('main'))
admin.add_url_rule('', view_func=AdminDashboardView.as_view('index'))
admin.add_url_rule('/settings', view_func=AdminDashboardView.as_view('settings'))
admin.add_url_rule('/', view_func=AdminDashboardView.as_view('users'))


class AdminSiteSettingsView(BaseView):
    _template = 'settings.html'

    decorators = [login_required]

    def get(self):
        from admin.forms import SiteSettingsForm
        from admin.models import SiteSetting
        settings = SiteSettings.query.all()
        self._form = SiteSettingsForm(obj=settings)



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

admin.add_url_rule('/add/page',view_func=AdminPageView.as_view('add_page'))
admin.add_url_rule('/edit/page/content',view_func=AdminPageView.as_view('page_content'))



class AdminTemplateView(BaseView):
    _template = 'add.html'
    _context = {'mce':True,
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
        AddTemplateForm = model_form(Template,db.session,base_class=Form,exclude=['blocks','pages','body'])
        class TemplateForm(AddTemplateForm):
            body = FormField(TemplateBodyFieldForm)

        self._form = TemplateForm
        return self.render()

    def post(self):
        from page.models import Template
        from auth.models import User
        from ext import db
        self._form = model_form(Template,db.session,base_class=Form,exclude=['blocks','pages','body'])(request.form)
        template = Template()
        self._form.populate_obj(template)
        template.save()
        filename = template.filename
        body = template.body[:]
        from settings import BaseConfig
        import os
        templatedir = os.path.join(BaseConfig.ROOT_PATH,'templates')
        os.system('touch {}'.format(os.path.join(templatedir,filename)))
        fp = open(os.path.join(templatedir,filename),'w')
        fp.write(body+'\n')
        fp.close()
        flash('you have created a new template named: {}'.format(template.name))
        return self.redirect('admin.templates')

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


            



admin.add_url_rule('/add/template',view_func=AdminTemplateView.as_view('add_template'))       


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



admin.add_url_rule('/add/block',view_func=AdminBlockView.as_view('add_block'))
admin.add_url_rule('/edit/block/content',view_func=AdminBlockView.as_view('block_content'))


class AdminCMSListView(BaseView):
    _template = 'list.html'
    _context = {}

    decorators = [login_required]
    
    def get(self):
        from settings import BaseConfig
        from page.models import Page,Block,Template
        from auth.models import User
        pp = BaseConfig.ADMIN_PER_PAGE
        if 'page' in request.endpoint:
            obj = Page
        if 'block' in request.endpoint:
            obj = Block
        if 'template' in request.endpoint:
            obj = Template
        objs = obj.query.all()
        if len(objs) > pp:
            return self.redirect('admin.page_{}'.format(obj.__name__.lower()),page_num=1)
        exclude = ['templates','pages','id','body','content',
                    'query','metadata','template','blocks',
                    'template_id','use_base_template','absolute_url',
                    'added_by']
        headings = obj.get_all_columns(exclude)
        self._context['objs'] = objs
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        return self.render()

admin.add_url_rule('/list/blocks',view_func=AdminCMSListView.as_view('blocks'))
admin.add_url_rule('/list/pages',view_func=AdminCMSListView.as_view('pages'))
admin.add_url_rule('/list/templates',view_func=AdminCMSListView.as_view('templates'))

class AdminListPageView(BaseView):
    _template = 'list.html'

    decorators = [login_required]

    def get(self,page_num=1):
        from admin.utils import Pagination
        from settings import BaseConfig
        pp = BaseConfig.ADMIN_PER_PAGE
        endpoint = request.endpoint
        if '_page' in endpoint:    
            from page.models import Page as model
        elif '_template' in endpoint:
            from page.models import Template as model
        else:
            from page.models import Block as model
        p = Pagination(model,page_num)
        self._context['objs'] = p._objs
        self._context['pagination'] = p
        exclude = ['templates','pages','id','body','content',
                    'query','metadata','template','blocks',
                    'template_id','use_base_template','absolute_url',
                    'added_by']
        headings = p._objs[0].get_all_columns(exclude)
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        self._context['codemirror'] = True
        return self.render()
admin.add_url_rule('/paged/page/<int:page_num>',view_func=AdminListPageView.as_view('page_page'))
admin.add_url_rule('/paged/template/<int:page_num>',view_func=AdminListPageView.as_view('page_template'))
admin.add_url_rule('/paged/block/<int:page_num>',view_func=AdminListPageView.as_view('page_block'))
        
        



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

admin.add_url_rule('/view/block/<name>',view_func=AdminDetailView.as_view('block_view'))
admin.add_url_rule('/view/page/<slug>',view_func=AdminDetailView.as_view('page_view'))
admin.add_url_rule('/view/template/<name>',view_func=AdminDetailView.as_view('template_view'))


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

admin.add_url_rule('/edit/block/<item_id>',view_func=AdminEditView.as_view('edit_block'))
admin.add_url_rule('/edit/page/<item_id>',view_func=AdminEditView.as_view('edit_page'))
admin.add_url_rule('/edit/template/<item_id>',view_func=AdminEditView.as_view('edit_template'))
admin.add_url_rule('/edit/page/content/<item_id>',view_func=AdminEditView.as_view('edit_page_content'))
admin.add_url_rule('/edit/block/content/<item_id>',view_func=AdminEditView.as_view('edit_block_content'))


class TestView(BaseView):
    _template = 'add.html'
    _form = None
    _context = {}

    def get(self):
        from admin.forms import TestForm
        self._form = TestForm
        self._form._has_pagedown = True
        self._context['url_link'] = 'admin.test'
        return self.render()


admin.add_url_rule('/test',view_func=TestView.as_view('test'))

class PageListView(BaseView):
    _template = 'list_pages.html'
    _context = {}

    def get(self):
        from page.models import Page
        pages = [FakePage(page) for page in Page.query.all()]
        self._context['page_list'] = pages
        return self.render()

admin.add_url_rule('/pages',view_func=PageListView.as_view('page_list'))

