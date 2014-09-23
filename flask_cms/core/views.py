# -*- coding: utf-8 -*-

"""
    core.views
    ~~~~~~~~~~
"""

from core import core
from main.baseviews import BaseView
from flask import flash, redirect, request, url_for
from admin.forms import AddPageForm
from blog.models import Category,Tag    
from .forms import MarkdownEditor
from settings import BaseConfig


class Column(object):
    _css = ''
    _content = ''
    _base_css = 'col-md-%d'
    _number = None

    def __init__(self,css=None,num=None):
        self.css = css
        if num is not None:
            self._number = num
            self.css = self._base_css % num

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self,content):
        self._content = content

    @property
    def number(self):
        return self._number
    

        

class IndexView(BaseView):
    _template = 'test2.html'
    _context = {'count':0,
            'l_count':0,
            }

    def get(self):
        from .forms import TestForm
        self._form = TestForm
        self._context['form'] = self._form()
        self._context['form_id'] = 'myForm'
        self._context['form']._name = 'myForm'

        self._context['cols'] = []
        self._context['rows'] = []
        count = 0
        for c in [2,1,4,1,10,2,10,2,5,5,2,2,4,4]:
            row = []
            col = Column(num=c)
            col.content = 'column ' + str(c) + '\njyvbuhkhvdliud bulz rvglzrglrvhgvl rhvrjkevg jhfgckzmj zhv\ndvavbeb'
            count = count + c
            if count <= 12:
                row.append(col)
            else:
                count = c
                self._context['rows'].append(row)
                row = []
                row.append(col)

            self._context['cols'].append(col)
        x = self.render()
        return x

    def post(self):
        self._context['layout_mode'] = True
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
        self._context['cat_form'] = AddCategoryForm()
        self._form.tags.query_factory = lambda: Tag.query.all()
        self._form.category.query_factory = lambda: Category.query.all()
        
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
        import datetime
        from .models import ContactMessage
        if len(request.args) > 0:
            message = ContactMessage()
            message.name = request.args['name']
            message.email = request.args['email']
            message.subject = request.args['subject']
            message.message = request.args['message']
            message.ip_address = request.environ['REMOTE_ADDR']
            message.save()
            self.flash("Thanks {} for sending us a message".format(request.args['name']))
        from page.forms import ContactUsForm
        from app import app
        self._context['CONTACT_FORM_SETTINGS'] = app.config.get('CONTACT_FORM_SETTINGS',None)
        ContactUsForm.subject.choices =  self._context['CONTACT_FORM_SETTINGS']['OPTIONS']
        self._form = ContactUsForm
        self._form_args = {'ip_address':request.environ['REMOTE_ADDR']}
        if self._context.get('mce'):
            self._context.pop('mce')
        return self.render()

class TestView(BaseView):
    _template = 'test.html'

    def get(self):
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

        
        
