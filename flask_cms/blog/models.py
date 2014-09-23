from sqlalchemy import desc
from flask import url_for
from LoginUtils import encrypt_password as generate_password_hash,check_password as  check_password_hash
from ext import db
import datetime
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
#from flask.ext.xxl.basemodels import BaseMixin
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
    #author = db.relationship('User',backref=db.backref(
    #                    'blogs',lazy='dynamic'))

    icon_id = db.Column(db.Integer,db.ForeignKey('font_icons.id'))
    icon = db.relationship('FontIcon',backref='blogs')


    @property
    def post_count(self):
        return len(self.posts)
    

    @staticmethod
    def get_by_author_id(author_id):
        return Blog.query.filter(Blog.author_id==author_id).all()

    def _get_absolute_url(self):
        return url_for('blog.post_list',item_id=self.id)

    def _get_edit_url(self):
        return url_for('admin.add_blog')
    
    def _get_create_url(self):
        return url_for('admin.add_blog')


class Tag(BaseMixin, db.Model):
    __tablename__ = 'tags'

    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    icon_id = db.Column(db.Integer,db.ForeignKey('font_icons.id'))
    icon = db.relationship('FontIcon',backref='tags')
    

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
    icon_id = db.Column(db.Integer,db.ForeignKey('font_icons.id'))
    icon = db.relationship('FontIcon',backref='categories')

    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_by_name(cls,name):
        return cls.query.filter(cls.name==name).first()


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
                        'articles',lazy='dynamic'),lazy='select')
    #author = db.relationship('User',backref="articles",lazy="dynamic")
    visible = db.Column(db.Boolean,default=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(255))
    url =  db.Column(db.String(255))
    meta_title =  db.Column(db.String(255))
    tags =  db.Column(db.String(255))


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



class Comment(BaseMixin,db.Model):
    __tablename__ = 'comments'

    slug = db.Column(db.String(255),nullable=False,unique=True)
    content = db.Column(db.Text,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    author = db.relationship('User',backref=db.backref(
                'comments',lazy="dynamic"))
    article_id = db.Column(db.Integer,db.ForeignKey('articles.id'))
    article = db.relationship('Article',backref=db.backref(
                'comments',lazy='dynamic'))

    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    post = db.relationship('Post',backref=db.backref(
                'comments',lazy='dynamic'))

    def __init__(self,*args,**kwargs):
        if kwargs.get('content',False):
            self.content = kwargs.pop('content')
        if kwargs.get('author_id',False):
            self.author_id = kwargs.pop('author_id')
        else:
            self.author_id = None
        if kwargs.get('article_id',False):
            self.article_id = kwargs.pop('article_id')
        else:
            self.article_id = None
        if kwargs.get('slug',False):
            self.slug = kwargs.pop('slug')
        else:
            tmp = '/comments/'
            if self.article_id is not None:
                tmp += self.article_id + '/'
            if self.author_id is not None:
                tmp += self.author_id + '/'
            self.slug = tmp
        super(Comment,self).__init__(*args,**kwargs)



class Post(BaseMixin,db.Model):
    __tablename__ = 'posts'

    name = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    blog = db.relationship('Blog',backref=db.backref(
                    'posts'),uselist=False)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    category = db.relationship('Category',backref=db.backref(
                    'posts'),uselist=False)
    #tags = db.relationship('Tag',secondary='posts_tags',backref=db.backref(
    #                'posts',lazy='dynamic'),lazy='dynamic')
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    author = db.relationship('User',backref=db.backref(
                    'posts'),uselist=False)
    date_added = db.Column(db.DateTime,default=db.func.now())
    date_modified = db.Column(db.DateTime,default=db.func.now(),onupdate=db.func.now())
    excerpt_length = db.Column(db.Integer,default=55,nullable=False)
    slug = db.Column(db.String(255),unique=True)
    icon_id = db.Column(db.Integer,db.ForeignKey('font_icons.id'))
    icon = db.relationship('FontIcon',backref='posts')

    @property
    def comment_count(self):
        return len(self.comments.query.all())

    @property 
    def author_name(self):
        return self.author.name or ''
    
    @property
    def title(self):
        return self.name.title()

    @property
    def excerpt(self):
        return self.content[:self.excerpt_length]

'''posts_tags = db.Table('posts_tags',db.metadata,
        db.Column('post_id',db.Integer,db.ForeignKey('posts.id')),
        db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
)

'''
