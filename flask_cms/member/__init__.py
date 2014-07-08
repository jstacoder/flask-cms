from flask import Blueprint

member = Blueprint('member',__name__,
                    template_folder='templates',
                    url_prefix='/<member_id>')


from views import *
