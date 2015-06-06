from flask import Blueprint

blog = Blueprint('blog',__name__,
                template_folder='templates',
                url_prefix='/blog')

try:
    from flask_cms.blog.views import *
except ImportError:
    pass

