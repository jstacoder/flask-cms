#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
"""
import subprocess
from flask import url_for
from flask.ext.script import Shell, Manager, prompt_bool
from flask.ext.script.commands import Clean,ShowUrls
from app import app
import urllib
import sqlalchemy_utils as squ
from flask.ext.alembic.cli.script import manager as alembic_manager
from get_files import get_templates, get_pyfiles
from flask_xxl.basemodels import BaseMixin as db
manager = Manager(app)



@manager.command
def show_routes():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "<{0}>".format(arg)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint,**options)
        line = urllib.unquote("{:30s} {:20s} {}".format(rule.endpoint,methods,url))
        output.append(line)
    for line in sorted(output):
        print line

@manager.command
def init_data():
    """Fish data for project"""
    if prompt_bool('Do you want to kill your db?'):
        if squ.database_exists(db.engine.url):
            squ.drop_database(db.engine.url)
    try:
        db.metadata.drop_all()
    except:
        pass
    try:
        squ.create_database(db.engine.url)
        db.metadata.create_all()
    except:
        pass

    user = User.query.filter(User.email=='kyle@level2designs.com').first()
    if user is None:
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
    app.test_request_context().push()
    manager.run()
