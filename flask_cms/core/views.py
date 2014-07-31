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


class IndexView(BaseView):
    _template = 'index.html'

    def get(self):
        return self.redirect('blog.blogs')


class AboutView(BaseView):
    _template = 'new_post.html'

    def get(self):
        self._form = AddPageForm()
        self._form.tags.query_factory = Tag.query.all
        self._form.category.query_factory = Category.query.all
        
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
