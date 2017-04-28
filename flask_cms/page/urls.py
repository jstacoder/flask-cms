from page import page
from .views import PagesView,AddPageView

routes = [
        ((page),
            ('/view/<obj_id>',PagesView.as_view('pages')),
            ('/view',PagesView.as_view('page')),
            ('/add_page',AddPageView.as_view('add_page')),
        )
    ]
