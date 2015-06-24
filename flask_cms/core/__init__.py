# -*- coding: utf-8 -*-
from flask import Blueprint

print 'imported as ',__name__
core = Blueprint('core', __name__,
                 template_folder='templates',
                 url_prefix='/')


from .views import *
