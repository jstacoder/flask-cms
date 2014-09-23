from jinja2 import Environment, StrictUndefined


jinja2_env = Environment(
    block_start_string="{{%",
    block_end_string="%}}",
    variable_start_string="{{{",
    variable_end_string="}}}",
    trim_blocks=True,
    undefined=StrictUndefined,
)

t = '''{{% if base %}}{% extends base %}{{% endif %}}\n
{% block body %}\n
{{% for col in cols %}}<div class=col>{% block col_{{{ loop.index }}} %}{% endblock %}</div>\n{{% endfor %}}\n
{% endblock %}
'''


template = jinja2_env.from_string(t)

print template.render(dict(base=True,cols=[1,2,3,4,5]))
