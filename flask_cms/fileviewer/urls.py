from flask_cms.fileviewer import fileviewer
from flask_cms.fileviewer.views import FileView
from flask_cms.fileviewer.json_tools import JsonCodeView

routes = [
        ((fileviewer),
            ('',FileView.as_view('view_files')),
            ('<item_name>',FileView.as_view('files')),
            ('/json',JsonCodeView.as_view('json')),
)]
