from flask import render_template,current_app
from core import core

@core.app_errorhandler(404)
def not_found(error):
    msg = 'Page Not Found'
    return render_template('errors.html',code=404,msg=msg), 404

@core.app_errorhandler(500)
def server_error(error):
    msg = 'Server Error, Whoops'
    return render_template('errors.html',code=500,msg=msg), 500 

@core.app_errorhandler(403)
def forbidden():
    msg = 'Access Denied!'
    return render_template('errors.html',code=403,msg=msg), 403

@core.app_errorhandler(503)
def service_unavailable():
    msg = 'service unavailable'
    return render_template('errors.html',code=503,msg=msg), 503


@core.before_app_request
def set_error_handler():
    if not current_app.error_handlers[404] == not_found:
        current_app.error_handlers[404] = not_found

