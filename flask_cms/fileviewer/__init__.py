from flask import Blueprint

fileviewer = Blueprint('fileviewer',__name__,
                        template_folder='templates',
                        url_prefix='/view_files')

from views import *
from flask_cms.fileviewer.models import *
