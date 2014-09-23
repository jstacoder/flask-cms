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
from ext import db
import urllib
import sqlalchemy_utils as squ
from flask.ext.alembic.cli.script import manager as alembic_manager
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
    from imports import (
            Widget,Article,Page,
            User,Setting,Type,
            Template,Tag,Role,
            Category,Block,Profile,
            ContactMessage)
    """Fish data for project"""
    if prompt_bool('Do you want to kill your db?'):
        if squ.database_exists(db.engine.url):
            squ.drop_database(db.engine.url)
    try:
        db.drop_all()
    except:
        pass
    try:
        squ.create_database(db.engine.url)
        db.create_all()
    except:
        pass

    user = User.query.filter(User.email=='kyle@level2designs.com').first()
    if user is None:
       user = User(username='kyle', email='kyle@level2designs.com', password='14wp88')
    user.save()


manager.add_command('shell', Shell(make_context=lambda:{'app': app, 'db': db}))


if __name__ == '__main__':
    manager.add_command('clean',Clean())
    manager.add_command('show_urls',ShowUrls())
    manager.add_command('db',alembic_manager)
    app.test_request_context().push()
    from imports import (
                    
                    Widget,Article,Page,
                    User,Setting,Type,
                    Template,Tag,Role,
                    Category,Block,AdminTab,Blog,
    )
    manager.run()
