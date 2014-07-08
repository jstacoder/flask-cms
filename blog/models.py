from sqlalchemy import desc
from LoginUtils import encrypt_password as generate_password_hash,check_password as  check_password_hash
from ext import db
import datetime
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
from basemodels import BaseMixin


class Tag(BaseMixin,db.Model):
    __tablename__ = 'tags'
    
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
 
    def __unicode__(self):
        return self.name

class Category(BaseMixin,db.Model):
    __tablename__ = 'categories'
    
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
 
    def __unicode__(self):
        return self.name
 
class Article(BaseMixin,db.Model):
    __tablename__ = 'articles'

    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    #category_name = db.Column(db.String(10), db.ForeignKey('categories.name'))
    #category = db.relationship('Category',primaryjoin='articles.category_name==categories.name')
    author_id = db.Column(db.Integer,db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))


    @classmethod
    def all(cls):
        return Article.query.order_by(desc(Article.created)).all()
 
    @classmethod
    def find_by_id(cls, id):
        return Article.query.filter(Article.id == id).first()
 
    @classmethod
    def find_by_author(cls, name):
        return Article.query.filter(Article.author_name == name).all()
 
    @classmethod
    def find_by_category(cls, category):
        return Article.query.filter(Article.category_name == category).all()
 
    @property
    def slug(self):
        return urlify(self.title)
 
    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)


def create_obj(obj_type,**kwargs):
    if obj_type == 'Article':
        return create_article(**kwargs)


def create_article(**kwargs):
    temp = Article()

    temp.title = kwargs.get('title')
    temp.body = kwargs.get('body')
    temp.category = kwargs.get('category')
    temp.author_id = kwargs.get('author_id')
    temp.save()
    return temp


