from . import fileviewer
from .views import FileView

routes = [
        ((fileviewer),
            ('',FileView.as_view('view_files')),
            ('<item_name>',FileView.as_view('files')),
)]
