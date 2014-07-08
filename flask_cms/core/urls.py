from core import core
from core.views import IndexView,AboutView,MeetView,ContactView

routes = [
    ((core,),
        ('',IndexView.as_view('index')),
        ('/about',AboutView.as_view('about')),
        ('meet',MeetView.as_view('meet')),
        ('contact',ContactView.as_view('contact')),
),
]
