from werkzeug.utils import import_string
from flask_cms.core import views
from flask_cms import core


routes = [
    ((core.core_blueprint,),
        ('',views.IndexView.as_view('index')),
        ('show/<layout_name>',views.IndexView.as_view('show_layout')),
        ('about',views.AboutView.as_view('about')),
        ('meet',views.MeetView.as_view('meet')),
        ('contact',views.ContactView.as_view('contact')),
        ('test',views.TestView.as_view('test')),
        ('new',views.NewView.as_view('new')),
        ('blockview/<int:alt_layout>',views.BlockView.as_view('blockview')),
        #('show_layout/<layout>',LayoutView.as_view('show_layout')),
        ('show_layout/<layout>/<navbar>',views.LayoutView.as_view('show_nav_layout')),
    )
]
