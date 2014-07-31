# -*- coding: utf-8 -*-

"""
    core blueprint for flask-cms
"""

from sqlalchemy.ext.declarative import declared_attr
from LoginUtils import encrypt_password as generate_password_hash
from LoginUtils import check_password as check_password_hash
from ext import db
from main.basemodels import BaseMixin

for attr in dir(db):
    globals()[attr] = getattr(db,attr)

class ContactMessage(BaseMixin,db.Model):
    __tablename__ = 'contact_messages'

    name = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    subject = Column(String(255),nullable=False)
    message = Column(Text)
    timestamp = Column(DateTime,default=func.now())
    ip_address = Column(String(20),nullable=False)


