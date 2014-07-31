from sqlalchemy import desc
from flask import url_for
from LoginUtils import encrypt_password as generate_password_hash,check_password as  check_password_hash
from ext import db
import datetime
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
from main.basemodels import BaseMixin


class Blog(BaseMixin, db.Model):
    __tablename__ = 'blogs'

    name = db.Column(db.String(255),nullable=False)
    title = db.Column(db.String(255),nullable=False)
    slug = db.Column(db.String(255),nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    category = db.relationship('Category',backref=db.backref(
                        'blogs',lazy='dynamic'))
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    author = db.relationship('User',backref=db.backref(
                        'blogs',lazy='dynamic'))

    @staticmethod
    def get_by_author_id(author_id):
        return Blog.query.filter(Blog.author_id==author_id).all()


class Tag(BaseMixin, db.Model):
    __tablename__ = 'tags'

    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)

    def __unicode__(self):
        return self.name

    @staticmethod
    def update_tags(tag_list):
        for tag in tag_list:
            t = Tag.query.filter(Tag.name==tag)
            if t is None:
                t = Tag()
                t.name = tag
                t.save()

    @property
    def link(self):
        return url_for('blog.tag_list',tag_id=self.id)


class Category(BaseMixin, db.Model):
    __tablename__ = 'categories'

    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)

    def __unicode__(self):
        return self.name


class Article(BaseMixin, db.Model):
    __tablename__ = 'articles'

    name = db.Column(db.String(255))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category',backref=db.backref(
        'articles',lazy='dynamic'))
    author_id = db.Column(db.Integer,db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    blog = db.relationship('Blog',backref=db.backref(
                        'posts',lazy='dynamic'),lazy='select')
    #author = db.relationship('User',backref="articles",lazy="dynamic")


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


