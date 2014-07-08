from flask import Blueprint

blog = Blueprint('blog',__name__,
                template_folder='templates',
                url_prefix='/blog')

try:
    from blog.views import *
except ImportError:
    pass

