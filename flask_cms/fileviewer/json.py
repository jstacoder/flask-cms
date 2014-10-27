from flask import jsonify,request,flash
from flask.json import loads
from flask.views import MethodView
import os.path as op


class JsonCodeView(MethodView):
    _SUCCESS_MESSAGE = 'You saved {}'
    _ERROR_MESSAGE = 'Error saving {}'

    def get(self):
        content = request.args.get('data[content]',None)
        file_name = request.args.get('data[file_name]',None)
        with open(file_name,'w') as f:
            f.write(content)
        success = op.isfile(file_name) and\
                open(file_name,'r').read() == content
        if success:
            flash(self._SUCCESS_MESSAGE.format(file_name),'success')
        else:
            flash(self._ERROR_MESSAGE.format(file_name),'danger')
        return jsonify(dict(success=success))


