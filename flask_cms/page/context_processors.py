import os
import jinja2
from flask import request, current_app, Markup, url_for


class IconLibNameConverter:
    _icon_librarys = dict(
            ionicon='ion',
            glyphicon='glyphicon',
            octicon='octicon',
            mfg_labs='icon',
            genericon='genericon',
            font_awesome='fa',
            elusive='el-icon',)

    _icon_sizes = dict(
        
        lg='fa-2x',
        xl='fa-3x',
        xxl='fa-4x',
        xxxl='fa-5x',
    )
    
    @staticmethod
    def parse_icon_size(size):
        if size in IconLibNameConverter._icon_sizes:
            return IconLibNameConverter._icon_sizes.get(size)
        return False

    @staticmethod
    def parse_icon_lib(lib_name):
        if lib_name in IconLibNameConverter._icon_librarys:
            return IconLibNameConverter._icon_librarys[lib_name]
        return False
    
    


def get_icon(icon,lib='glyphicon',fw=False,size=None):
    lib = IconLibNameConverter.parse_icon_lib(lib)
    if fw:
        html = '<span class="{0} {0}-{1}-fw'
    else:
        html = '<span class="{0} {0}-{1}'
    if size is not None:
        html = html + ' ' + IconLibNameConverter.parse_icon_size(size) + '"></span>'
    else:
        html = html + '"></span>'
    return Markup(html.format(lib,icon))

def add_get_icon():
    return dict(get_icon=get_icon)
    
def add_page_self_context():
    if 'page' in request.endpoint:
        from .models import Page
        get_page = lambda slug: Page.query.filter(Page.slug == slug).first()
        if request.view_args:
            if request.view_args.get('slug', False):
                slug = request.view_args['slug']
                return {"self": get_page(slug)}
    return {"self": False}


def add_get_block():
    from .models import StaticBlock
    get_block = lambda block_id: StaticBlock.query.filter(StaticBlock.block_id == block_id).first()()
    return {
        'get_block': get_block
    }


def is_page(obj):
    return obj.__class__.__name__ == 'Page'


def add_is_page():
    return {'is_page': is_page}

_BUTTON_DEFAULTS = dict(
    text='',
    color='grey',
    size='sm',
    type="button",
)

def get_button(name):
    from jinja2 import Template
    from .models import Button
    button = Button.query.get(Button.get_id_by_name(name))
    if button is None:
        return Markup('<a class="btn btn-default">{}</a>'.format(name))
    else:
        btn_args = dict(
            text=button.text,
            color=button.color,
            size=button.size.lower(),
            icon=button.icon,
            lib=button.icon_library,
            type=button.type
        )
    template = Template(open(os.path.join(current_app.config['ROOT_PATH'], 'templates', 'buttons.html'), 'r').read())
    def url_for(*args,**kwargs):
        return '/admin'
    return Markup(template.render(args=btn_args,url_for=url_for))


def add_get_button():
    return {'get_button': get_button}


@jinja2.contextfunction
def _get_context(c):
    return c


def get_context():
    return {'get_context': _get_context}


def add_urlfor():
    return dict(url_for=url_for)
