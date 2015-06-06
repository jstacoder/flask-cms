# -*- coding: utf-8 -*-

"""
    core blueprint for flask-cms
"""

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column,Text,String,DateTime,func,Text
from LoginUtils import encrypt_password as generate_password_hash
from LoginUtils import check_password as check_password_hash
from flask_xxl.basemodels import BaseMixin


class ContactMessage(BaseMixin):

    name = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    subject = Column(String(255),nullable=False)
    message = Column(Text)
    timestamp = Column(DateTime,default=func.now())
    ip_address = Column(String(20),nullable=False)


