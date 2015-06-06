from flask_cms.blog import blog
from flask_cms.blog.views import (
        BlogIndexView,BlogAdminView,ModalEditView,
        AddView,MemberArticleView,TagListView,
        SinglePostView,PostListView,BlogListView,
        AddPostView,
)

routes = [
        ((blog),
            ('/',BlogIndexView.as_view('index')),
            #('/bloglist',BlogAdminView.as_view('member.admin_list',member_id=1)),
            ('/bloglist',BlogAdminView.as_view('list')),
            ('/taglist/<tag_id>',TagListView.as_view('tag_list')),
            ('/edit/<id>',ModalEditView.as_view('edit')),
            ('/add',AddView.as_view('add')),
            ('/blogs',MemberArticleView.as_view('blogs')),
            #('/blog/<blog_id>',MemberArticleView.as_view('post_list')),
            ('/post/<post_id>',MemberArticleView.as_view('post_detail')),
            ('/post/<post_id>/edit',MemberArticleView.as_view('post_edit')),
            ('/blog/<blog_id>/edit',MemberArticleView.as_view('blog_edit')),
            ('/blog/<int:item_id>',PostListView.as_view('post_list')),
            ('/post/<int:item_id>',SinglePostView.as_view('view_post')),
            ('/add_post',AddPostView.as_view('add_post')),
        )
    ]
