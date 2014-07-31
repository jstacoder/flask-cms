from main.baseviews import BaseView
from .forms import AddTemplateForm
from flask import request

class AdminTemplateView(BaseView):
    _template = 'add.html'
    _context = {}
    _form = AddTemplateForm

    def get(self,item_id=None):
        from page.models import Block,Page,Macro
        from page.models import Template
        # if we have an id this is an edit view
        if item_id is None:
            # create_view
            # there should be a name given through ajax
            name = request.args.get('name',None)
            self._form_args = {'name':name}
        else:
            template = Template.query.get_or_404(item_id)
            self._form_obj = template
        return self.render()

    def post(self,item_id=None):
        from page.models import Template
        if self._form().validate():
            template = Template(name=self._form().name.data,body=self._form().body.data)
            template.save()
            self.flash("created new template")
        return self.redirect('admin.index')
