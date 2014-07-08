# -*- coding: utf-8 -*-

"""
    main.py - where the magic happens
    ~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import os
from flask import Flask
from werkzeug.utils import import_string

class NoRouteModuleException(Exception):
    pass

class NoTemplateFilterException(Exception):
    pass

class NoContextProcessorException(Exception):
    pass

class NoBlueprintException(Exception):
    pass

class NoExtensionException(Exception):
    pass

class AppFactory(object):

    def __init__(self, config, envvar='PROJECT_SETTINGS', bind_db_object=True):
        self.app_config = config
        self.app_envvar = os.environ.get(envvar, False)
        self.bind_db_object = bind_db_object

    def get_app(self, app_module_name, **kwargs):
        self.app = Flask(app_module_name, **kwargs)
        self.app.config.from_object(self.app_config)
        self.app.config.from_envvar(self.app_envvar, silent=True)

        self._bind_extensions()
        self._register_routes()
        self._register_blueprints()
        self._register_context_processors()
        self._register_template_filters()

        return self.app

    def _get_imported_stuff_by_path(self, path):
        module_name, object_name = path.rsplit('.', 1)
        module = import_string(module_name)

        return module, object_name

    def _bind_extensions(self):
        for ext_path in self.app.config.get('EXTENSIONS', []):
            module, e_name = self._get_imported_stuff_by_path(ext_path)
            if not hasattr(module, e_name):
                raise NoExtensionException('No {e_name} extension found'.format(e_name=e_name))
            ext = getattr(module, e_name)
            if getattr(ext, 'init_app', False):
                ext.init_app(self.app)
            else:
                ext(self.app)

    def _register_template_filters(self):
        for filter_path in self.app.config.get('TEMPLATE_FILTERS', []):
            module, f_name = self._get_imported_stuff_by_path(filter_path)
            if hasattr(module, f_name):
                self.app.jinja_env.filters[f_name] = getattr(module, f_name)
            else:
                raise NoTemplateFilterException('No {f_name} template filter found'.format(f_name=f_name))

    def _register_context_processors(self):
        for processor_path in self.app.config.get('CONTEXT_PROCESSORS', []):
            module, p_name = self._get_imported_stuff_by_path(processor_path)
            if hasattr(module, p_name):
                self.app.context_processor(getattr(module, p_name))
            else:
                raise NoContextProcessorException('No {cp_name} context processor found'.format(cp_name=p_name))

    def _register_blueprints(self):
        self._bp = []
        for blueprint_path in self.app.config.get('BLUEPRINTS', []):
            module, b_name = self._get_imported_stuff_by_path(blueprint_path)
            if hasattr(module, b_name):
                self.app.register_blueprint(getattr(module, b_name))
            else:
                raise NoBlueprintException('No {bp_name} blueprint found'.format(bp_name=b_name))

    def _register_routes(self):
        for url_module in self.app.config.get('URL_MODULES',[]):
            module,r_name = self._get_imported_stuff_by_path(url_module)
            if hasattr(module,r_name):
                self._setup_routes(getattr(module,r_name))
            else:
                raise NoRouteModuleException('No {r_name} url module found'.format(r_name=r_name))

    def _setup_routes(self,routes):
        for route in routes:
            blueprint,rules = route[0],route[1:]
            for pattern, view in rules:
                blueprint[0].add_url_rule(pattern,view_func=view)
            if blueprint[0] in self._bp:
                self.app.register_blueprint(blueprint[0])

