from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import datetime
 
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
 
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=True)
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    age = db.Column(db.Integer)
    pwdhash = db.Column(db.String(100))
 
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
 
    def __repr__(self):
        return '<Person %r>' % (self.firstname)
 
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
 
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
 
    def __unicode__(self):
        return self.name

    @classmethod
    def all(cls):
        return cls.query.all()
 
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship(Category)
    person_name = db.Column(db.String(100), db.ForeignKey(Person.firstname, onupdate="CASCADE", ondelete="CASCADE"))
    person = db.relationship(Person,foreign_keys='[Post.person_name]')
    author_id = db.Column(db.Integer,db.ForeignKey('person.id'))
    visible = db.Column(db.Boolean,default=False)

    @property
    def category_name(self):
        return self.category.name

    @property
    def author(self):
       return self.person_name

    @property
    def markup(self):
        return self.body

    @markup.setter
    def set_markup(self,data):
        self.body = data[:]

    @classmethod
    def all(cls):
        return Post.query.order_by(desc(Post.created)).all()
 
    @classmethod
    def find_by_id(cls, id):
        return Post.query.filter(Post.id == id).first()
 
    @classmethod
    def find_by_author(cls, name):
        return Post.query.filter(Post.person_name == name).all()
 
    @classmethod
    def find_by_category(cls, category):
        return Post.query.filter(Post.category_name == category).all()
 
    @classmethod
    def find_by_tag(cls, tag):
        return Tag.posts.query.filter('post.person = cls.person').all()

    @property
    def slug(self):
        return urlify(self.title)
 
    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,db.Sequence('user_id_seq'),primary_key=True)
    name = db.Column(db.String(255),nullable=False,unique=True)
    description = db.Column(db.Text)

    def __unicode__(self):
        return self.name

    @classmethod
    def all(cls):
        return cls.query.all()

posts_tags = db.Table('posts_tags',db.metadata,
        db.Column('post_id',db.ForeignKey('post.id')),
        db.Column('tags_id',db.ForeignKey('tags.id'))
)

