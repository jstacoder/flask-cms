#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
"""
import subprocess
from flask import url_for
from flask_script import Shell, Manager, prompt_bool
from flask_script.commands import Clean,ShowUrls
from app import app
import urllib
import os
import sqlalchemy_utils as squ
from flask_alembic.cli.script import manager as alembic_manager
from get_files import get_templates, get_pyfiles
from flask_xxl.basemodels import BaseMixin as db
from flask_cms.auth.models import User
manager = Manager(app)



@manager.command
def show_routes():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "<{0}>".format(arg)
        methods = ','.join(rule.methods)
        url = rule.rule #url_for(rule.endpoint,**options)
        line = urllib.unquote("{:40s} {:30s} {}".format(rule.endpoint,methods,url))
        output.append(line)
    for line in sorted(output):
        print line

@manager.command
def init_data():
    with app.test_request_context():
        db.metadata = User.metadata
        db.metadata.bind = User.engine	   
        user = User.query.filter(User.email=='kyle@level2designs.com')
        if user.count() > 0:
            user = User(username='kyle', email='kyle@level2designs.com', password='test')
            user.save()


manager.add_command('shell', Shell(make_context=lambda:{'app': app, 'db': db}))

class DBClass(object):
    def __init__(self,cls):
        self.db = cls

if __name__ == '__main__':
    app.extensions = app.extensions or {}
    app.extensions['sqlalchemy'] = DBClass(db)
    manager.add_command('clean',Clean())
    manager.add_command('show_urls',ShowUrls())
    manager.add_command('db',alembic_manager)
    get_templates = manager.command(get_templates)
    get_pyfiles = manager.command(get_pyfiles)
    #print os.environ.get('DATABASE_URL')
    #items = [(k, app.config[k]) for k in app.config.keys()]
    #for item in items:
    #    print item
    with app.test_request_context():

        User.metadata.bind = User.engine
        manager.run()
