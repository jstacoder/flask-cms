from jinja2 import Environment, StrictUndefined

def get_env():
    jinja2_env = Environment(
        block_start_string="{{%",
        block_end_string="%}}",
        variable_start_string="{{{",
        variable_end_string="}}}",
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return jinja2_env

class Column(object):
    _num = None;
    _name = None;

    def __init__(self,num,name):
        self._name = name
        self._num = num

    @property
    def name(self):
        return self._name

    @property
    def num(self):
        return self._num


def get_env_template(string):
    return get_env().from_string(string)


def get_template(string,**kwargs):
    return get_env_template(string).render(**kwargs)


def add_col(num,name):
    return get_env().from_string('<div class=col-md-{{{col_num}}}>{% block {{{ block_name }}} %}{% endblock %}</div>').render(col_num=num,block_name=name)


def get_row(cols=[]):
    rtn = '<div class=row>' + '\n'
    for col in cols:
        rtn += add_col(col.num,col.name)+'\n' 
    rtn = rtn + '</div>'
    return rtn

t = '''{{% if base %}}{% extends base %}{{% endif %}}
{% block body %}
{{% for col in cols %}}<div class=col>{% block col_{{{ loop.index }}} %}{% endblock %}</div>\n{{% endfor %}}
{% endblock %}
'''


#template = jinja2_env.from_string(t)

#print template.render(dict(base=True,cols=[1,2,3,4,5]))

cols = [
    Column(3,'test1'),
    Column(4,'test2'),
]

print get_row(cols)
