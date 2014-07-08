# define bluepriont specific context processors

def example_context():
    return {'example':'value'}

def nav():
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

def frontend_nav():
    return {'nav_links':
            (
                ('core.index','Home'),
                ('blog.index','Blog'),
                ('core.meet','Meet Us'),
                ('core.about','About'),
                ('core.contact','Contact'),
            ),
            'nav_title':'My Site',
    }

def admin_nav():
    return {'admin_nav_links':
            (
                ('Admin','admin.index'),
                ('Pages','page.page'),
                ('template','admin.add_template'),
                ('Settings','admin.settings'),
                ('Manage Users','admin.users'),
            ),
            'admin_nav_title':'Site Admin',
            'admin_dropdowns':(
            
                dict(
                    List=dict(
                                    Blocks='admin.blocks',
                                    Pages='admin.pages',
                                    Templates='admin.templates',
                              )
                    ),
                dict(
                    Add=dict(
                                    Template='admin.add_template',
                                    Page='admin.add_page',
                                    Block='admin.add_block',
                              )
                    ),),
                }




# frontend nav title


#def admin_title():
#    return {'admin_title':'Admin'}
# register this in settings.py to make it avialible in all templates
