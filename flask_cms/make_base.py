from flask import url_for,g,session, current_app
import os
from jinja2.environment import Template

root = lambda: current_app.config.get('ROOT_PATH',None)

def get_flask_context():
    return {'g':g,'url_for':url_for,'session':session,'config':current_app.config,'root':root()}

def get_imports(import_list):
    res = ''
    for filename,macro in import_list:
        #res += '{% from "' + filename + '" import ' + macro + ' %}' + '\n'
        res += open(os.path.join(root(),'core','templates',filename),'r').read() + '\n'
    return res

def start_head():
    return '''<!doctype html>
<html>
    <head>
        <meta charset='utf-8' />
    '''

def get_bootstrap_css(cdn=True):
    if cdn:
        rtn = '''
        <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.css" />
        <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap-theme.css" />
        <link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet" />
        '''
    else:
        rtn = '''
        <link rel="stylesheet" href="{{ url_for('static',filename='css/bootstrap.css')}}" />
        <link rel="stylesheet" href="{{ url_for('static',filename='css/bootstrap-theme.css')}}"/>
        <link rel="stylesheet" href="{{ url_for('static',filename='css/font-awesome.css')}}" />
        {% block extra_head %}{% endblock extra_head %}
        '''
    return rtn


def get_css(file_list=[]):
    rtn = '<link rel="stylesheet" href="{{url_for(\'static\',filename=\'css/style.css\')}}" />\n'
    for filename in file_list:
        rtn +=\
                '        <link rel="stylesheet" type="text/css" href="{{ url_for(\'static\',filename=\'css/' + filename + '\')}}" />\n'
    return rtn

def get_title():
    return '''        <title>
        {% if title -%}
        {{ title }}
        {% else %}
        {% block title %}
        {% endblock title %}
        {%- endif %}
        </title>
        '''

def get_extra_head():
    return '''
    <script type="text/javascript">
        var SCRIPT_ROOT = "{{request.url_root}}";
    </script>
    {% block js_head %}{% endblock js_head %}
    {% block extra_head %}{% endblock extra_head %}
    '''

def end_head():
    return '    </head>'

def get_head(css_files=[],bootstrap_cdn=True,**kwargs):
    rtn = ''
    rtn += get_imports(kwargs.pop('import_list')) + '\n'
    rtn += start_head() + '\n'
    rtn += get_bootstrap_css(bootstrap_cdn) + '\n'
    rtn += get_css(css_files) + '\n'
    rtn += get_title() + '\n'
    rtn += get_extra_head() + '\n'
    rtn += end_head() + '\n'
    return rtn

def get_body(jquery_version=''):
    rtn = '''
    <body id=body {% block body_style %} style="{% if body_style %}{{ body_style }}{% else %}padding-top:60px;{% endif %}"{% endblock body_style %}>
        {% block body %}{% endblock body %}
        {% if layout_mode %}{{ layout_menu()|safe }}{% endif %}
        {% if logged_in %}{{ admin_head() }}{% endif %}
        <script type="text/javascript" src="http://code.jquery.com/jquery.'''
    rtn = rtn + jquery_version
    if jquery_version != '':
        rtn = rtn + '.'
    rtn = rtn + '''js"></script>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.js"></script>
        {% block footer_js %}{% endblock footer_js %}
    </body>
</html>
    '''
    return rtn

def get_base(*args,**kwargs):
    rtn = get_head(*args,**kwargs)
    rtn += get_body()
    return Template(rtn)

def base():
    # add css files here    V
    return {
        'base' : get_base(
            css_files = [
                'elusive-webfont.css',
                'octicons.css',
                'blog_admin.css',
                'font-awesome.css',
                'mfglabs_iconset.css',
                'ionicons.css',
                'genericons.css',
            ],
            import_list = [
                (
                    'macros/navbar.html',
                    'render_nav',
                )
            ],
        )
    } 



'''
        {% if not admin %}
            <div class=container-fluid>
        {% endif %}
        {% block header %}
        {% include 'includes/_header.html' with context %}
        {% endblock header %}
        {% if admin %}
            <div class=container-fluid>
        {% endif %}
        {% block messages %}
        {% include 'includes/_messages.html' %}
        {% endblock messages %}
        <div class=row>
        {% block body %}{% endblock body %}
        {% block content %}{% endblock content %}
        {% block sidebar %}{% endblock sidebar %}
    </div>
        {% block footer %}{% endblock footer %}
            </div>
        {% block footer_js %}
        <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
        <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.js">
            </script>
        {% if form %}
            {% set ck = false %}
            {% for f in form %}
                {% if f.type == 'CKTextEditorField' %}
                    {% set ck = true %}
                {% endif %}
            {% endfor %}
            {% if ck %}
                <script src="{{url_for('static',filename='js/ckeditor/ckeditor.js')}}"></script>
                <script type="text/javascript">
                    CKEDITOR.replace( 'ckeditor', {extraPlugins: 'codemirror',startupMode : 'source'} );
                </script>
            {% endif %}
        {% endif %}
            {% if mce %}
            <script src="//tinymce.cachefly.net/4.0/tinymce.min.js"></script>
            <script type="text/javascript">
                tinymce.init({
                    selector: "textarea"
                    });
            </script>
            {% endif %}
        {% endblock footer_js %}
    </body>
</html>
<!doctype html>
<html>
    <head>
        <style>
        /*
        * Style tweaks
        * --------------------------------------------------
        */
        html,
        body {
            overflow-x: hidden; /* Prevent scroll on narrow devices */
            }
            body {
                padding-top: 70px;
                }
            footer {
                    padding: 30px 0;
                }

    .jumbotron {
        background: #358CCE;
        color: #FFF;
        border-radius: 0px;
    }
    .jumbotron-sm { padding-top: 24px;
        padding-bottom: 24px; }
    .jumbotron small {
        color: #FFF;
    }
    .h1 small {
        font-size: 24px;
    }
    .col-md-2 {
        padding-right:0px!important;
    }
       /*
        * Off Canvas
        * --------------------------------------------------\
        */
        @media screen and (max-width: 767px) {
        .row-offcanvas {
            position: relative;
            -webkit-transition: all .25s ease-out;
   7         -o-transition: all .25s ease-out;
            transition: all .25s ease-out;
        }

        .row-offcanvas-right {
            right: 0;
        }

        .row-offcanvas-left {
            left: 0;
        }

        .row-offcanvas-right
        .sidebar-offcanvas {
            right: -50%; /* 6 columns */
        }

        .row-offcanvas-left
        .sidebar-offcanvas {
            left: -50%; /* 6 columns */
        }

        .row-offcanvas-right.active {
            right: 50%; /* 6 columns */
        }
    }

        </style>
        <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.css" />
        <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap-theme.css" />
        {#<link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}" />#}
        {% if title %}
            <title>{{ title }}</title>
        {% endif %}
        {% block js_head %}
        {% endblock js_head %}
        {% block extra_head %}
        {% endblock extra_head %}
    </head>
    <body style="{% if body_style %}{% block body_style %}{{ body_style }}{% endblock body_style %}{% else %}padding-top:60px;{% endif %}">
        {% block meta_nav %}{% endblock meta_nav %}
        {% if not admin %}
        <div class="container{% if wide %}-fluid{% endif %}">
        {% endif %}
        {% block header %}
        {% include 'includes/_header.html' with context %}
        {% endblock header %}
        {% if admin %}
            <div class=container-fluid>
        {% endif %}
        {% block messages %}
        {% include 'includes/_messages.html' %}
        {% endblock messages %}
        {#{% block sidebar %}{% endblock sidebar %}#}
        {% block body %}{% endblock body %}
        {% block content %}{% endblock content %}
        {% block footer %}{% endblock footer %}
            </div>
        {% block footer_js %}
        {#<script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>#}
            <script src="http://174.140.227.137:8080/_debug_toolbar/static/js/jquery.js"></script>
            <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.js">
            </script>
            <script src="//tinymce.cachefly.net/4.0/tinymce.min.js"></script>
            <script type="text/javascript">
                tinymce.init({
                    selector: "textarea"
                    });
            </script>
        {% endblock footer_js %}
    </body>
</html>
<!doctype html>
<html>
    <head>
        <style>
            {% if admin is defined %}
            body { padding-top:75px;}
            {% endif %}
        </style>
        <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.css" />
        <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap-theme.css" />
        {% set ck = false %}
        {% if form %}            
            {% for f in form %}
                {% if f.type == 'FormField' %}
                    {% for field in f %}
                        {% if field.type == 'CKTextEditorField' %}
                            {% set ck = true %}
                        {% endif %}
                    {% endfor %}
                {% elif f.type == 'CKTextEditorField' %}
                        {% set ck = true %}
                {% endif %}
            {% endfor %}
        {% endif %}
        {% if not ck %}
        
        {% endif %}
        {#<link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}" />#}
        {% if title is defined %}
            <title>{{ title }}</title>
        {% endif %}
        <script type="text/javascript">
            var $SCRIPT_ROOT = {{ request.url_root|tojson|safe }};
            var SCRIPT_ROOT = {{ request.url_root|tojson|safe }};
        </script>
        {% block extra_head %}
        {% endblock extra_head %}
    </head>
    <body style="{% if body_style %}{% block body_style %}{{ body_style }}{% endblock body_style %}{% else %}padding-top:75px;{% endif %}">
        {% if not admin %}
            <div class=container>
        {% endif %}
        {% block header %}
            {% include 'admin/_header.html' with context %}
        {% endblock header %}
        {% if admin %}
            <div class=container>
        {% endif %}
        {% block messages %}
            {% include 'includes/_messages.html' with context %}
        {% endblock messages %}
        {% block body %}{% endblock body %}
        {% block content %}{% endblock content %}
                <footer>

                    {% block footer %}{% endblock footer %}
                </footer>
            </div>
        {% block footer_js %}
            
            <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
            <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.js">
            </script>
        {% if form %}
            {% set ck = false %}
            {% for f in form %}
                {% if f.type == 'FormField' %}
                    {% for field in f %}
                        {% if field.type == 'CKTextEditorField' %}
                            {% set ck = true %}
                        {% endif %}
                    {% endfor %}
                {% elif f.type == 'CKTextEditorField' %}
                        {% set ck = true %}
                {% endif %}
            {% endfor %}
        {% if codemirror %}
            {#{{ codemirror.include_codemirror() }}#}
        {% endif %}
            {% if ck %}                
                <script src="{{url_for('static',filename='js/ckeditor/ckeditor.js')}}"></script>
                <script type="text/javascript">
                    CKEDITOR.replace( 'ckeditor', {extraPlugins: 'codemirror',startupMode : 'source'});
                </script>
            {% endif %}        
        {% endif %}
        {% endblock footer_js %}
    </body>
</html>
'''
