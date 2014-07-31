# -*- coding: utf-8 -*-

"""
    core.tests
"""

from flask import url_for
from .testing import KitTestCase


class TestFrontBlueprint(KitTestCase):

    def test_front(self):
        response = self.client.get(url_for('core.index'))
        self.assert200(response)

    def test_front_for_anonymous(self):
        response = self.client.get(url_for('core.index'))
        self.assertContains(response, 'Log in')

    def test_login(self):
        response = self.client.get(url_for('core.login'))
        self.assert200(response)
