# -*- coding: utf-8 -*-

"""
    core blueprint for flask-cms
"""

from sqlalchemy.ext.declarative import declared_attr
from LoginUtils import encrypt_password as generate_password_hash
from LoginUtils import check_password as check_password_hash
from ext import db
from basemodels import BaseMixin

for attr in dir(db):
    globals()[attr] = getattr(db,attr)

