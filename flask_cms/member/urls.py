from member import member
from .views import MemberArticleView,MemberProfileView

routes = [
        ((member),
            ('/blogs',MemberArticleView.as_view('blog_list')),
            ('/blog/<blog_id>',MemberArticleView.as_view('post_list')),
            ('/post/<post_id>',MemberArticleView.as_view('post_detail')),
            ('/post/<post_id>/edit',MemberArticleView.as_view('post_edit')),
            ('/blog/<blog_id>/edit',MemberArticleView.as_view('blog_edit')),
            ('/profile',MemberProfileView.as_view('profile')),
        )
    ]
