from main.baseviews import BaseView
from flask import request, jsonify

class SaveStaticBlockView(BaseView):

    def get(self):
        from page.models import StaticBlock
        name = request.args.get('name')
        block_id = request.args.get('block_id')
        content = request.args.get('content')
        block = StaticBlock.get_by_block_id(block_id)
        if block is None:
            block = StaticBlock()
            block.name = name
            block.block_id = block_id
        block.content = content
        try:
            block.save()
            return jsonify({'success':True,'error':False})
        except:
            return jsonify({'error':True,'success':False})

class SaveSuccessStaticBlockView(BaseView):
    def get(self):
        self.flash('saved static block')
        return self.redirect('admin.list_static_block')

class SaveErrorStaticBlockView(BaseView):
    def get(self):
        self.flash('error saving static block')
        return self.redirect('admin.list_static_block')

class SaveSuccessAdminTabView(BaseView):
    def get(self):
        self.flash("you created a new admin tab")
        return self.redirect('admin.index')

class SaveErrorAdminTabView(BaseView):
    def get(self):
        self.flash('error saving admin tab')
        return self.redirect('admin.index')

