from baseviews import BaseView
from flask.templating import render_template_string
from menu import context_processors 
from flask import request
from page import page

admin_required = ''

class PagesView(BaseView):
    _template = ''
    _context = {}
    _base_template = 'aabout.html'

    def render(self):
        return render_template_string(self._template,**self._context)


    def get(self,slug):
        from auth.models import User
        from page.models import Page
        page = Page.get_by_slug(slug)
        self._page = page
        self.frontend_nav()
        self._context['content'] = page.content
        blocks = self._page.blocks.all()
        #self._page.template.process_blocks(blocks)
        if page.use_base_template:
            self._template = "{{template}}"
            self._template = render_template_string(self._template,template=self._base_template)
            self._template =  "{% extends '" + self._template + "' %}<br />{% block body %}{% endblock body %}<br />"
        return self.render()

    def post(self,slug):
        from auth.models import User
        from page.models import Page
        page = Page.get_by_slug(request.url.split('/')[-1])
        page = Page.get_by_slug(slug)
        data = request.form.get('content')
        if data != page.content:
            page.content = data
            page.update()
        self._page = page
        self.frontend_nav()
        self._context['content'] = page.content
        if page.use_base_template:
            self._process_base_template()
        return self.render()
        
    def _process_base_template(self):
        self._template = "{{template}}"
        self._template = render_template_string(self._template,template=self._base_template)
        self._template =  "{% extends '" + self._template + "' %}<br />{% block body %}{% endblock body %}<br />"

    def frontend_nav(self):
        self._setup_nav()

    def _setup_sidebar(self):
        if self._page.add_to_sidebar:
            sidebar_data = []
            pages = self._page.query.all()
            for page in pages:
                if page.add_to_sidebar:
                    sidebar_data.append(
                        ((page.name,'pages.page',dict(slug=page.slug)))
                    )        
            #self._context['sidebar_data'] = ('Title',sidebar_data)
        
    def _setup_nav(self):
        self._context['nav_links'] = []
        pages = self._page.query.all()
        for page in pages:
            if page.add_to_nav:
                self._context['nav_links'].append(
                        (('page.pages',dict(slug=page.slug)),'{}'.format(page.name))
                )
        self._context['nav_title'] = '{}'.format(self._page.title)
        self._setup_sidebar()
        
page.add_url_rule('/view/<slug>',view_func=PagesView.as_view('pages'))
page.add_url_rule('/view',view_func=PagesView.as_view('page'))


