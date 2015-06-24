from sqlalchemy import desc,Column,String,DateTime,Integer,ForeignKey,Text,Boolean,func
from sqlalchemy.orm import backref,relationship
from flask import url_for
from LoginUtils import encrypt_password as generate_password_hash,check_password as  check_password_hash
import datetime
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
from flask_xxl.basemodels import BaseMixin

class Blog(BaseMixin):

    name = Column(String(255),nullable=False)
    title = Column(String(255),nullable=False)
    slug = Column(String(255),nullable=False)
    category_id = Column(Integer,ForeignKey('categories.id'))
    category = relationship('Category',backref=backref(
                        'blogs',lazy='dynamic'))
    author_id = Column(Integer,ForeignKey('users.id'))
    #author = relationship('User',backref=backref(
    #                    'blogs',lazy='dynamic'))

    icon_id = Column(Integer,ForeignKey('font_icons.id'))
    icon = relationship('FontIcon',backref='blogs')


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


class Tag(BaseMixin):

    name = Column(String(100), unique=True)
    description = Column(Text)
    icon_id = Column(Integer,ForeignKey('font_icons.id'))
    icon = relationship('FontIcon',backref='tags')
    

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


class Category(BaseMixin):
    name = Column(String(100), unique=True)
    description = Column(Text)
    icon_id = Column(Integer,ForeignKey('font_icons.id'))
    icon = relationship('FontIcon',backref='categories')

    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_by_name(cls,name):
        return cls.query.filter(cls.name==name).first()


class Article(BaseMixin):
    name = Column(String(255))
    title = Column(String(100))
    content = Column(Text)
    date_added = Column(DateTime, default=datetime.datetime.now)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category',backref=backref(
        'articles',lazy='dynamic'))
    author_id = Column(Integer,ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))
    blog_id = Column(Integer,ForeignKey('blogs.id'))
    blog = relationship('Blog',backref=backref(
                        'articles',lazy='dynamic'),lazy='select')
    #author = relationship('User',backref="articles",lazy="dynamic")
    visible = Column(Boolean,default=False)
    description = Column(Text)
    slug = Column(String(255))
    url =  Column(String(255))
    meta_title =  Column(String(255))
    tags =  Column(String(255))


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



class Comment(BaseMixin):

    slug = Column(String(255),nullable=False,unique=True)
    content = Column(Text,nullable=False)
    author_id = Column(Integer,ForeignKey('users.id'))
    author = relationship('User',backref=backref(
                'comments',lazy="dynamic"))
    article_id = Column(Integer,ForeignKey('articles.id'))
    article = relationship('Article',backref=backref(
                'comments',lazy='dynamic'))

    post_id = Column(Integer,ForeignKey('posts.id'))
    post = relationship('Post',backref=backref(
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



class Post(BaseMixin):

    name = Column(String(255),nullable=False)
    content = Column(Text)
    blog_id = Column(Integer,ForeignKey('blogs.id'))
    blog = relationship('Blog',backref=backref(
                    'posts'),uselist=False)
    category_id = Column(Integer,ForeignKey('categories.id'))
    category = relationship('Category',backref=backref(
                    'posts'),uselist=False)
    #tags = relationship('Tag',secondary='posts_tags',backref=backref(
    #                'posts',lazy='dynamic'),lazy='dynamic')
    author_id = Column(Integer,ForeignKey('users.id'))
    author = relationship('User',backref=backref(
                    'posts'),uselist=False)
    date_added = Column(DateTime,default=func.now())
    date_modified = Column(DateTime,default=func.now(),onupdate=func.now())
    excerpt_length = Column(Integer,default=55,nullable=False)
    slug = Column(String(255),unique=True)
    icon_id = Column(Integer,ForeignKey('font_icons.id'))
    icon = relationship('FontIcon',backref='posts')

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

'''posts_tags = Table('posts_tags',db.metadata,
        db.Column('post_id',db.Integer,db.ForeignKey('posts.id')),
        db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
)

'''
