# -*- coding: utf-8 -*-

"""
    core.views
    ~~~~~~~~~~
"""
#from recaptcha.client import captcha
from flask_xxl.baseviews import BaseView
from flask import flash, redirect, request, url_for,jsonify,session
from flask_cms.blog.models import Category,Tag
from .forms import MarkdownEditor, ColumnForm
from flask_cms.settings import BaseConfig
from flask_cms.admin.forms import AddPageForm
from test_jinja import main,row,col
from jinja2 import Template

'''
class AddRowView(BaseView):
    # ajax only view, no template

    def get(self):
        cols = request.args.get('cols',None)
        rows = request.args.get('rows',None)
'''

class IndexView(BaseView):
    _template = '1_col_left.html'#'test_grid.html'#'new22.html'#'blog3.html'#'layouts/1col_leftsidebar.html'
    _context = {
            'add_buttons':True,
            'count':0,
            'l_count':0,
            'body_style':'padding-top:75px;',

    }
    _row = (
                row('660',cols=[
                    col(2),col(8),col(2)
                ]),
        ),        

    _form = ColumnForm




    def get(self,layout_name=None):
        self._args = request.args.get('layout',False)
        #if self._args:
        #    self._template = Template(main(self._args))
        #else:
        #    self._template = Template(main())
        self._layouts = {
            'one_col_empty':(col(12),),
            'one_col_leftbar':(col(2),col(10)),
            'one_col_rightbar':(col(10),col(2)),
            'one_col_both':(col(2),col(8),col(2)),
            'two_col_empty':(col(6),col(6)),
            'two_col_leftbar':(col(2),col(5),col(5)),
            'two_col_rightbar':(col(5),col(5),col(2)),
            'two_col_both':(col(2),col(4),col(4),col(2)),
            'three_col_empty':(col(4),col(4),col(4)),
            'three_col_leftbar':(col(2),col(3),col(3),col(4)),
            'three_col_rightbar':(col(4),col(3),col(3),col(2)),
        }
        #from admin.forms import CreateGridForm
        #self._form = CreateGridForm
        #self._context['form_id'] = 'myForm'

        #content = (row('660',cols=(col(2),col(8),col(2))),)
        #footer = (row('140',cols=(col(3),col(6),col(3))),)
        
        #if layout_name is not None:
        #    self._context['rows'] = (row('660',cols=list(self._layouts[layout_name.replace('-','_')])),) + footer
        #else:
        #    self._context['rows'] = content + footer

        #self._context['layouts'] = self._layouts.keys()
        x = self.render()
        return x

    def post(self):
        self._context['f'] = request.files.copy()
        if ColumnForm(request.form).validate():
            self._context['offset'] = request.form.get('offset',None)
            self._context['push'] = request.form.get('push',None)
            self._context['pull'] = request.form.get('pull',None)
            self._context['width'] = request.form.get('col_width',None)
        #self._context['layout_mode'] = True
        return self.render()

class BlockView(BaseView):
    _template = '3g.html'

    def get(self,alt_layout=None):
        if alt_layout is not None:
            if int(alt_layout) in [3,4,5]:
                self._template = '{}g.html'.format(alt_layout)
        return self.render()


class LayoutView(BaseView):
    _context = {'body_style':'',
                'navbar_file_in_context':True,
                'navbar_name':'clean'}

    def get(self,layout=None,navbar=None):
        if navbar:
            self._context['navbar_name'] = navbar
        if layout is None:
            flash('invalid request')
            return self.redirect('core.index')
        self._template = BaseConfig.LAYOUT_FILES[layout]
        if not self._template:
            flash('That layout does not exist')
            return self.redirect('core.index')
        return self.render()


class AboutView(BaseView):
    _template = 'new_post.html'

    def get(self):
        from blog.forms import AddCategoryForm
        self._form = AddPageForm(last_url=request.endpoint)
        args = request.args.copy()
        if 'icon' in args:
            icon = args.get('icon')
            desc = args.get('description')
            cat = args.get('name')
            self._context['cat_form'] = AddCategoryForm(name=cat,description=desc,icon=icon)
            self._context['category_launch'] = True
            self._context['args'] = args
        else:
            self._context['cat_form'] = AddCategoryForm()
        self._form.tags.query_factory = lambda: Tag.query.all()
        self._form.category.query_factory = lambda: Category.query.all()
        self._context['editor_mode'] = 'python'
        
        return self.render()

    def post(self):
        self._context['content'] = request.form.get('content')
        return self.render()


class MeetView(BaseView):
    _template = 'jumbo.html'

    def get(self):
        return self.render()



class ContactView(BaseView):
    _template = 'contact.html'
    _form = None
    _context = {}

    def get(self):
        error = False

        import datetime
        from .models import ContactMessage
        if len(request.args) > 0:
            #captcha_challenge = request.args.get('recaptcha_challenge_field',None)
            #captcha_response = request.args.get('recaptcha_response_field',None)
            #if captcha_challenge and captcha_response:
            #    captcha_result = captcha.submit(
            #        captcha_challenge,
            #        captcha_response,
            #        BaseConfig.RECAPTCHA_PRIVATE_KEY,
            #        request.environ['REMOTE_ADDR']
            #    )
            #    if captcha_result.is_valid:
            #        message = ContactMessage()
            #        message.name = request.args['name']
            #        message.email = request.args['email']
            #        message.subject = request.args['subject']
            #        message.message = request.args['message']
            #        message.ip_address = request.environ['REMOTE_ADDR']
            #        message.save()
            #        self.flash("Thanks {} for sending us a message".format(request.args['name']),'info')
            #    else:
            #        flash('bad captcha response try again','danger')
            #        error = True
            #
            #else:
            #    flash('please enter captcha value','warning')
            #    error = True
            message = ContactMessage()
            message.name = request.args['name']
            message.email = request.args['email']
            message.subject = request.args['subject']
            message.message = request.args['message']
            message.ip_address = request.environ['REMOTE_ADDR']
            message.save()
            self.info("Thanks {} for sending us a message".format(request.args['name']))
            #    else:
            #        flash('bad captcha response try again','danger')
            #        error = True
        if error:
            session['has_message_data'] = True
            session['message.name'] = request.args.get('name','')
            session['message.email'] = request.args.get('email','')
            session['message.subject'] = request.args.get('subject','')
            session['message.message'] = request.args.get('message','')

        from page.forms import ContactUsForm
        from app import app
        self._context['CONTACT_FORM_SETTINGS'] = app.config.get('CONTACT_FORM_SETTINGS',None)
        ContactUsForm.subject.choices =  self._context['CONTACT_FORM_SETTINGS']['OPTIONS']
        self._form = ContactUsForm
        self._form_args = {'ip_address':request.environ['REMOTE_ADDR']}
        if session.get('has_message_data',False):
            session['has_message_data'] = False
            self._form_args.update(dict(
                name=session.get('message.name',''),
                email=session.get('message.email',''),
                subject=session.get('message.subject',''),
                message=session.get('message.message',''),
            )
        )
        if self._context.get('mce'):
            self._context.pop('mce')
        return self.render()

class TestView(BaseView):
    _template = 'utest.html'

    def get(self):
        from flask import request
        self._context['f'] = request
        return self.render()

    def post(self):
        from flask import request
        self._context['f'] = request
        return self.render()



class NewView(BaseView):
    _template = 'new.html'

    def get(self):
        self._context['itms'] = ('item1','item2','item3','item4')
        return self.render()


class MarkDownView(BaseView):
    _template = 'markdown.html'
    _form = MarkdownEditor
    _context = {}

    def get(self,filename=None):
        content = ''
        if filename is not None:
            if os.path.exists(filename):
                content = open(filename,'r').read()
        self._context['content'] = content
        return self.render()

        
        
class GridView(BaseView):

    _grid_file = 'admin/templates/make_grid.html'

    def __init__(self,*args,**kwargs):
        self._setup_jinja()
        super(GridView,self).__init__(*args,**kwargs)
    
    def _setup_jinja():
        from jinja2 import Environment, BaseLoader
        self.jinja2_env = Environment(
            block_start_string="{{%",
            block_end_string="%}}",
            variable_start_string="{{{",
            variable_end_string="}}}",
            trim_blocks=True,
        )

    def _get_grid(self):
        from flask import request

        args = request.args.copy()
        row_count = 0
        col_count = 0
        for k,v in args.items:
            if 'row' == k:
                pass




#return jinja2_env.from_string(open('admin/templates/make_grid.html','r').read()).render(dict(rows=content+footer,fluid=True,wide=True,body_style=''))


class JsonRequestView(BaseView):

    def get(self):
        import json
        args = request.args.copy()
        step = args.pop('step')
        if int(step) == 1:
            self._template = 'step1-' +  args.get('rows') + '.html'
        else:
            self._template = 'step' + step + '.html'
            self._context['args'] = args
        x = self.render()
        return jsonify(dict(html=x))


class TaskView(BaseView):
    _tasks = None
    _template = 'task.html'
    _format = '''
                <a class="list-group-item">
                    <div class="checkbox">
                        <label>
                           <input type="checkbox" class="checkbox" {} />{}
                        </label>
                     </div>
                 </a>
                '''

    def get(self):
        if request.args.get('tasks',None) is not None:
            self._context['tasks'] = request.args.get('tasks')
        return self.render()

    def post(self):
        session['title'],session['tasks'] = self._render_task_list(request.form.get('text',''))        
        return redirect(url_for('.tasks'))


    def _render_task_list(self,text):
        rtn = ''
        lines = text.splitlines()
        title = lines.pop(0).title()
        for line in lines:
            rtn += self._format.format('',line)
        return (title,'<div class=list-group>'+rtn+'</div>')
