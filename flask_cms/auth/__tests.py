from ..testing import TC
from flask import url_for
from main.factory import AppFactory
from settings import TestingConfig


class AuthBlueprintTestClass(TC):

    def create_app(self):
        return AppFactory(TestingConfig).get_app(__name__)

    def test_login(self):
        response = self.client.post(url_for('auth.login'),params=dict(email='kyle@level2designs.com',password='14wp88'))
        self.assert200(response)
