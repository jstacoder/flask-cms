# -*- coding: utf-8 -*-

"""
    core.tests
"""
from flask_xxl.main import AppFactory
from flask import url_for
from flask.ext.testing import TestCase
from flask_cms.settings import TestingConfig
import sqlalchemy_utils as squ
from twill.browser import TwillBrowser
from flask_cms.testing import TC

class TestFrontBlueprint(TC):

    #def create_app(self):
    #    return AppFactory(TestingConfig).get_app(__name__)
       
    #def setUp(self):
    #    from imports import (Widget,
    #            Page,User,Setting,
    #            Type,Template,Tag,
    #            Role,Category,Block,
    #            Profile,ContactMessage,
    #            Blog,Macro,Button,StaticBlock,
    #            TemplateBlock,AdminTab,Post,Article)
    #
    #   self.browser = TwillBrowser()
    #    squ.create_database(self.app.extensions['sqlalchemy'].db.engine.url)
    #    self.app.extensions['sqlalchemy'].db.create_all()

    #def tearDown(self):
    #    self.app.extensions['sqlalchemy'].db.session.remove()
    #    self.app.extensions['sqlalchemy'].db.drop_all()
    #    squ.drop_database(self.app.extensions['sqlalchemy'].db.engine.url)

    def test_front(self):
        response = self.client.get(url_for('core.index'))
        self.assert200(response)

    def test_front_for_anonymous(self):
        response = self.client.get(url_for('auth.login'))
        self.assertContains(response, 'Sign In')

    def test_login(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_admin_redirect(self):
        res = self.client.get(url_for('admin.index'))
        self.assertTrue('Redirect' in res.data)
