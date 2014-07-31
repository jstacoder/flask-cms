from admin import admin
from .views2 import AdminTemplateView as AddAdminTemplateView
from .views import (AdminDashboardView,AdminPageView,AdminTemplateView,AdminBlockView,
                    AdminCMSListView,AdminListPageView,AdminDetailView,AdminEditView,
                    PageListView,AdminBlogView,AdminAddCategoryView,AdminAddBlogView)


routes = [
        ((admin),
            ('',AdminDashboardView.as_view('index')),
            ('/template/add',AddAdminTemplateView.as_view('template_add')),
            ('/template/add/item_id',AddAdminTemplateView.as_view('template_edit')),
            ('/settings',AdminDashboardView.as_view('settings')),
            ('/add/category',AdminAddCategoryView.as_view('add_category')),
            ('/add/page',AdminPageView.as_view('add_page')),
            ('/add/blog',AdminAddBlogView.as_view('add_blog')),
            ('/edit/page/content',AdminPageView.as_view('page_content')),
            ('/add/template',AdminTemplateView.as_view('add_template')),
            ('/add/block',AdminBlockView.as_view('add_block')),
            ('/edit/block/content',AdminBlockView.as_view('block_content')),
            ('/list/blocks',AdminCMSListView.as_view('blocks')),
            ('/list/pages',AdminCMSListView.as_view('pages')),
            ('/list/users',AdminCMSListView.as_view('users')),
            ('/list/templates',AdminCMSListView.as_view('templates')),
            ('/paged/page/<int:page_num>',AdminListPageView.as_view('page_page')),
            ('/paged/user/<int:page_num>',AdminListPageView.as_view('page_users')),
            ('/paged/template/<int:page_num>',AdminListPageView.as_view('page_template')),
            ('/paged/block/<int:page_num>',AdminListPageView.as_view('page_block')),
            ('/view/block/<name>',AdminDetailView.as_view('block_view')),
            ('/view/page/<slug>',AdminDetailView.as_view('page_view')),
            ('/view/template/<name>',AdminDetailView.as_view('template_view')),
            ('/edit/block/<item_id>',AdminEditView.as_view('edit_block')),
            ('/edit/page/<item_id>',AdminEditView.as_view('edit_page')),
            ('/edit/template/<item_id>',AdminEditView.as_view('edit_template')),
            ('/edit/page/content/<item_id>',AdminEditView.as_view('edit_page_content')),
            ('/edit/block/content/<item_id>',AdminEditView.as_view('edit_block_content')),
            ('/pages',PageListView.as_view('page_list')),
            ('/blogs',AdminBlogView.as_view('blogs')),
        )
    ]
