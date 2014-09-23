from settings import BaseConfig
from flask import g
from core.context_processors import get_model
# define blueprint specific context processors


def example_context():
    return {'example': 'value'}

'''def admin_nav():
    brand = 'Admin'
    nav_links = {
            'Home':'index',
            'Files':'index',
            'Other':'index'
            }

    dropdowns = {
            'Dropdown One':{
                'nothing':'index',
                'more':'index',
                'sep':None,
                'more nothing':'admin'
            }
        }
'''


def frontend_nav():
    return {
        'nav_links':
        (
            ('core.index', 'Home'),
            ('blog.index', 'Blog'),
            ('core.meet', 'Meet Us'),
            ('core.about', 'About'),
            ('core.contact', 'Contact'),
        ),
        'nav_title': 'My Site',
    }

def admin_nav():
    return {'admin_nav_links':
                        (
                            ('AdminDashBoard', 'admin.index'),
                        ),
                        
            'admin_nav_title': 'Admin',

            'admin_dropdowns':((
                    ('Manage',[
                        ('Users','admin.users',),
                        ('Blogs','admin.blogs',),
                        ('Settings','admin.settings',),
                    ]),                                    
                    ('List',[
                        ('BlogPosts','admin.blogs'),
                        ('StaticBlocks','admin.list_static_block'),
                        ('Blocks','admin.blocks'),
                        ('Pages','admin.pages'),
                        ('Templates','admin.templates'),
                        ('Buttons','admin.buttons'),
                        ('sep',None),
                        ('AllIcons','admin.all_icons'),
                        ('Glyphicons',('admin.icons_by_lib',dict(lib='glyphicon'))),
                        ('FontAwesome',('admin.icons_by_lib',dict(lib='fa'))),
                        ('Octicons',('admin.icons_by_lib',dict(lib='octicon'))),
                        ('ElusiveIcons',('admin.icons_by_lib',dict(lib='el-icon'))),
                ]),
                ('Add',[
                        ('Template','admin.add_template'),
                        ('Page','admin.add_page'),
                        ('Macro','admin.add_macro'),
                        ('Blog','admin.add_blog'),
                        ('Buttons','admin.add_button'),
                        ('StaticBlock','admin.add_static_block'),
                        ('AdminTabs','admin.add_tab'),
                    ]),
                ),)                            
            }


def sidebar():
    get_sidebar_tabs = [x.tab_id for x in get_model('admin_tab','admin').query.all()]
    return dict(
        sidebar_links=
        (
            get_sidebar_tabs,
           
        )
    )


def get_navbar():
    nav_id = g.get('nav_id', None) or BaseConfig.DEFAULT_NAVBAR
    for itm in BaseConfig.NAVBAR_TEMPLATE_FILES:
        if nav_id == itm[0]:
            return {'navbar': itm[1]}



def _get_navbar(name=None):
    if name is None:
        name = BaseConfig.DEFAULT_NAVBAR
    for itm in BaseConfig.NAVBAR_TEMPLATE_FILES:
        if name == itm[0]:
            return itm[1]

def _add_navbar():
    return dict(_get_navbar=_get_navbar)



# frontend nav title
'''
('Blogs', 'blog-tab'),
('add page', 'page-tab'),
('Macros', 'macro-tab'),
('add post', 'post-tab'),
'''

#def admin_title():
#    return {'admin_title':'Admin'}
# register this in settings.py to make it avialible in all templates
