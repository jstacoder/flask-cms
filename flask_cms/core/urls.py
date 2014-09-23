from core import core
from core.views import IndexView,MeetView,ContactView,TestView,AboutView,NewView,BlockView,LayoutView


routes = [
    ((core,),
        ('',IndexView.as_view('index')),
        ('about',AboutView.as_view('about')),
        ('meet',MeetView.as_view('meet')),
        ('contact',ContactView.as_view('contact')),
        ('test',TestView.as_view('test')),
        ('new',NewView.as_view('new')),
        ('blockview/<int:alt_layout>',BlockView.as_view('blockview')),
        ('show_layout/<layout>',LayoutView.as_view('show_layout')),
        ('show_layout/<layout>/<navbar>',LayoutView.as_view('show_nav_layout')),
    )
]
