from core import core
from core.views import IndexView,MeetView,ContactView,TestView,AboutView,NewView
from auth import auth


routes = [
    ((core,),
        ('',IndexView.as_view('index')),
        ('about',AboutView.as_view('about')),
        ('meet',MeetView.as_view('meet')),
        ('contact',ContactView.as_view('contact')),
        ('test',TestView.as_view('test')),
        ('new',NewView.as_view('new')),
    )
]
