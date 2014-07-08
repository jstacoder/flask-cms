# -*- coding: utf-8 -*-

"""
    core.views
    ~~~~~~~~~~
"""

from core import core
from baseviews import BaseView
from flask import flash, redirect, request, url_for



class IndexView(BaseView):
    _template = 'index.html'

    def get(self):
        return self.redirect('blog.blogs')

core.add_url_rule('', view_func=IndexView.as_view('index'))

class AboutView(BaseView):
    _template = 'about.html'

    def get(self):
        return self.render()
    def post(self):
        self._context['content'] = request.form.get('content')
        return self.render()

core.add_url_rule('about',view_func=AboutView.as_view('about'))

class MeetView(BaseView):
    _template = 'meet_us.html'

    def get(self):
        return self.render()
core.add_url_rule('meet',view_func=MeetView.as_view('meet'))



class ContactView(BaseView):
    _template = 'contact.html'
    _form = None
    _context = {}
    
    def get(self):
        if len(request.args) > 0:
            self._context['args'] = {'email':request.args['email']}
        from page.forms import ContactUsForm
        from app import app
        self._context['CONTACT_FORM_SETTINGS'] = app.config.get('CONTACT_FORM_SETTINGS',None)
        ContactUsForm.subject.choices =  self._context['CONTACT_FORM_SETTINGS']['OPTIONS']
        self._form = ContactUsForm
        if self._context.get('mce'):
            self._context.pop('mce')
        return self.render()
core.add_url_rule('contact',view_func=ContactView.as_view('contact'))

class TestView(BaseView):
    _template = 'test.html'

    def get(self):
        return self.render()


core.add_url_rule('test',view_func=TestView.as_view('test'))
