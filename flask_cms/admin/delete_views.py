from main.baseviews import BaseView
from flask import request, jsonify

class DeleteStaticBlockView(BaseView):
    _response = {
            'success':True,
            'error':None
    }

    def get(self):
        from page.models import StaticBlock
        block = StaticBlock.get_by_block_id(request.args.get('block_id',None))
        if block is None:
            self._response['success'] = False
            self._response['error'] = 'No block found with id: ' + request.args.get('block_id','ERROR')
            self.flash("no block found?")
        else:
            try:
                bname = block.name
                block.delete()
                self.flash('Deleted: ' + bname)
            except Exception, e:
                self._response['success'] = False
                self._response['error'] = 'Error while deleting block with id: ' + request.args.get('block_id','ERROR')
                self.flash("error deleting:\n" + str(e))
        return jsonify(self._response)


