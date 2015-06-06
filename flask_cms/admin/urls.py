from flask_cms.admin import admin
from flask_cms.admin.views import (
        AdminDashboardView,AdminPageView,
        AdminTemplateView,AdminBlockView,
        AdminCMSListView,AdminListPageView,
        AdminDetailView,AdminEditView,
        PageListView,AdminBlogView,AdminAddCategoryView,
        AdminAddBlogView,AdminAddButtonView,
        AdminShowButtonView,AdminStaticBlockView,
        AdminAddMacroView,AdminCodeView,AdminTemplateAjaxView,
        AdminBlogListView,AdminListedView,AdminModalView,TestView,
        AdminTabView,AdminFilesystemView,AdminSiteSettingsView,IconView,
)
from flask_cms.admin.save_views import (
        SaveStaticBlockView,SaveSuccessStaticBlockView,
        SaveErrorStaticBlockView,SaveSuccessAdminTabView,
        SaveErrorAdminTabView,
)

from flask_cms.admin.delete_views import (
        DeleteStaticBlockView
)

from flask_cms.admin.views2 import AdminTemplateView as AddAdminTemplateView
'''from .views import (AdminDashboardView,AdminPageView,AdminTemplateView,AdminBlockView,
                    AdminCMSListView,AdminListPageView,AdminDetailView,AdminEditView,
                    PageListView,AdminBlogView,AdminAddCategoryView,AdminAddBlogView)'''


routes = [
        ((admin),
            ('',AdminDashboardView.as_view('index')),
            ('/files',AdminFilesystemView.as_view('files')),
            ('/test',TestView.as_view('test')),
            ('/button/<item_id>',AdminShowButtonView.as_view('view_button')),
            ('/settings',AdminSiteSettingsView.as_view('settings')),
            ('/template/add',AddAdminTemplateView.as_view('template_add')),
            ('/template/add/item_id',AddAdminTemplateView.as_view('template_edit')),
            ('/add/category',AdminAddCategoryView.as_view('add_category')),
            ('/add/page',AdminPageView.as_view('add_page')),
            ('/add/admin_tab',AdminTabView.as_view('add_tab')),
            ('/add/blog',AdminAddBlogView.as_view('add_blog')),
            ('/edit/page/content',AdminPageView.as_view('page_content')),
            ('/add/template',AdminTemplateView.as_view('add_template')),
            ('/add/block',AdminBlockView.as_view('add_block')),
            ('/edit/block/content',AdminBlockView.as_view('block_content')),
            ('/list/blocks',AdminCMSListView.as_view('blocks')),
            ('/list/blogs',AdminCMSListView.as_view('blogs')),
            ('/list/pages',AdminCMSListView.as_view('pages')),
            ('/list/users',AdminCMSListView.as_view('users')),
            ('/list/templates',AdminCMSListView.as_view('templates')),
            ('/list/buttons',AdminCMSListView.as_view('buttons')),
            ('/paged/page/<page_num>',AdminListPageView.as_view('page_page')),
            ('/paged/user/<page_num>',AdminListPageView.as_view('page_users')),
            ('/paged/template/<page_num>',AdminListPageView.as_view('page_template')),
            ('/paged/block/<page_num>',AdminListPageView.as_view('page_block')),
            ('/view/block/<name>',AdminDetailView.as_view('block_view')),
            ('/view/page/<slug>',AdminDetailView.as_view('page_view')),
            ('/view/template/<name>',AdminDetailView.as_view('template_view')),
            ('/edit/block/<item_id>',AdminEditView.as_view('edit_block')),
            ('/edit/page/<item_id>',AdminEditView.as_view('edit_page')),
            ('/edit/template/<item_id>',AdminEditView.as_view('edit_template')),
            ('/edit/page/content/<item_id>',AdminEditView.as_view('edit_page_content')),
            ('/edit/block/content/<item_id>',AdminEditView.as_view('edit_block_content')),
            ('/pages',PageListView.as_view('page_list')),
            #('/blogs',AdminBlogView.as_view('blog')),
            #('/blogs',AdminBlogListView.as_view('blog')),
            ('/blogs',AdminListedView.as_view('blog')),
            ('/button/add',AdminAddButtonView.as_view('add_button')),
            ('/add/static_block',AdminStaticBlockView.as_view('add_static_block')),
            ('/list/static_block',AdminStaticBlockView.as_view('list_static_block')),
            ('/add/macro',AdminAddMacroView.as_view('add_macro')),
            ('/edit/static_block/<item_id>',AdminStaticBlockView.as_view('edit_static_block')),
            ('/list/code',AdminCodeView.as_view('list_code')),
            ('/edit/file/<path:file_path>',AdminCodeView.as_view('edit_file')),
            ('/get/template',AdminTemplateAjaxView.as_view('get_base')),
            ('/modal',AdminModalView.as_view('modal')),
            ('/save/success/static_block',SaveSuccessStaticBlockView.as_view('save_static_block_success')),
            ('/save/error/static_block',SaveErrorStaticBlockView.as_view('save_static_block_error')),
            ('/save/static_block',SaveStaticBlockView.as_view('save_static_block')),
            ('/delete/static_block',DeleteStaticBlockView.as_view('delete_static_block')),
            ('/save/success/admin_tab',SaveSuccessAdminTabView.as_view('save_admin_tab_success')),
            ('/save/error/admin_tab',SaveErrorAdminTabView.as_view('save_admin_tab_error')),
            ('/icons',IconView.as_view('icons')),
            ('/icons/<lib>',IconView.as_view('icons_by_lib')),
            ('/allicons',IconView.as_view('all_icons')),
        )
    ]
