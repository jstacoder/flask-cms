from . import fileviewer
from .views import FileView
from .json import JsonCodeView

routes = [
        ((fileviewer),
            ('',FileView.as_view('view_files')),
            ('<item_name>',FileView.as_view('files')),
            ('/json',JsonCodeView.as_view('json')),
)]
