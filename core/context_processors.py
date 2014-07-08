# -*- coding: utf-8 -*-

"""
    core.context_processors
"""
from flask.helpers import url_for

def common_context():
    return {            
            'my_email': 'kyle@level2designs.com',
            'type':type,
            'dir':dir,
            }


def common_forms():
    return {}


def is_page(obj):
    return obj.__class__.__name__ == 'Page'


def add_is_page():
    return {'is_page':is_page}
