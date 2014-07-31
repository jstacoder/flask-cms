from main.basemodels import BaseMixin
import datetime
from ext import db
from flask import url_for
from flask.templating import render_template_string as render_str
import pickle
from sqlalchemy.ext.hybrid import hybrid_property
from jinja_tools import Block as BlockBase

for attr in dir(db):
    globals()[attr] = getattr(db,attr)


pages_macros = Table('pages_macros',
    Column('page_id',Integer,ForeignKey('pages.id')),
    Column('macro_id',Integer,ForeignKey('macros.id'))
)

class Page(BaseMixin,Model):
    __tablename__ = 'pages'

    name = Column(String(255))
    description = Column(Text)
    template_id = Column(Integer,ForeignKey('templates.id'))
    template = relationship('Template',backref=backref(
                'pages',lazy='dynamic'))
    slug = Column(String(255))
    title = Column(String(255))
    add_to_nav = Column(Boolean,default=False)
    add_left_sidebar = Column(Boolean,default=False)
    add_right_sidebar = Column(Boolean,default=False)
    date_added = Column(DateTime,default=datetime.datetime)
    visible = Column(Boolean,default=False)
    meta_title = Column(String(255))
    added_by = relationship('User',backref=backref(
        'pages',lazy='dynamic'))
    user_id = Column(Integer,ForeignKey('users.id'))
    short_url = Column(String(255))
    macros = relationship('Macro',secondary='pages_macros',
                            backref=backref('pages',lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        if self.name is None:
            rtn = '<Page: Unnamed | {}'.format(self.line_count)
        else:
            rtn = '<Page: {} | {} lines'.format(self.name,self.line_count)
        return rtn

    def _get_page_url(self):
        return url_for('page.pages',slug=self.slug)

    @staticmethod
    def _get_create_url():
        return url_for('admin.add_page')

    @classmethod
    def get_by_slug(cls,slug):
        return cls.query.filter(cls.slug==slug).first()

    def _get_absolute_url(self):
        return url_for('admin.page_view',slug=self.slug)

    def _get_edit_url(self):
        return url_for('admin.edit_page',item_id=int(self.id))

    def _get_edit_content_url(self):
        return url_for('admin.edit_page_content',item_id=int(self.id))

    @property
    def line_count(self):
        try:
            rtn = len(self.content.split('\n'))
        except:
            rtn = 0
        return rtn

    @property
    def template_name(self):
        return self.template.name or ''

    @property
    def block_count(self):
        return self.template.blocks.count()

    @property
    def blocks(self):
        return self.template.blocks.keys()


class Template(BaseMixin,Model):
    __tablename__ = 'templates'

    name = Column(String(255),nullable=False,unique=True)
    description = Column(Text)
    body = Column(Text)
    base_template = Column(String(255))
    

    def __init__(self,*args,**kwargs):
        self._raw_template = ''
        self._head = ''
        for attr in ['name','body','filename']:
            tmp = kwargs.pop(attr,None)
            if tmp is not None:
                self.__dict__[attr] = attr
        base = kwargs.pop('base_template',None)
        if base is None:
            self.is_base_template = True
        else:
            self.is_base_template = False
            self._add_to_head(self._create_extend(base))
        if self.body:
            self._set_template()

    def _add_to_head(self,itm):
        self._head = self._head + '\n' + itm

    def _create_extend(self,parent):
        return '{% extends "%s" %}' % parent

    def _set_template(self):
        from jinja2 import Template
        self._raw_template = Template(self._head + self.body[:])

    @property
    def block_count(self):
        return len(self._raw_template.blocks)

    @property
    def blocks(self):
        return self._raw_template.blocks.keys()

    def set_body(self,data):
        self.body = data
        self._set_template()

    @property
    def body_body(self):
        return self.body

    @property
    def content(self):
        return self.body[:]

    def _get_edit_url(self):
        return url_for('admin.edit_template',item_id=int(self.id))

    def _get_absolute_url(self):
        return url_for('admin.template_view',name=self.name)

    def __repr_(self):
        if self.name is None:
            rtn = '<Template: Unnamed | {} lines'.format(self.line_count)
        else:
            rtn = '<Template: {} | {} lines'.format(self.name,self.line_count)
        return rtn

    def __str__(self):
        return self.body or ''

    @staticmethod
    def _get_create_url():
        return url_for('admin.add_template')

    @property
    def line_count(self):
        try:
            rtn = len(self.body.split('\n'))
        except:
            rtn = 0
        return rtn


    def get_block_count(self):
        return len(self._raw_template.blocks.keys())
    
    @staticmethod
    def get_base_templates():
        return []

class Block(BaseMixin,Model):
    __tablename__ = 'blocks'

    name = Column(String(255))
    content = Column(Text)

    def __init__(self,name='',content=''):
        self.name = name
        self.content = content


    @property
    def head(self):
        start = '{% block '
        mid = self.name
        end = ' %}'
        return start + mid + end

    @property
    def foot(self):
        start = '{% endblock '
        mid = self.name
        end = ' %}'
        return start + mid + end

    def set_content(self,data):
        self.content = data

    def __call__(self):
        return self.render()

    def __str__(self):
        return self.head + '\n' + self.content + '\n' + self.foot

    def render(self):
        s = self.content.split('\n')
        return self.head + '<br />'.join(map(str,s)) + self.foot

    def __repr__(self):
        if self.name is None:
            rtn = '<Block: Unnamed | {} lines'.format(self.line_count)
        else:
            rtn = '<block: {} | {} lines'.format(self.name,self.line_count)
        return rtn


    @staticmethod
    def _get_create_url():
        return url_for('admin.add_block')

    def _get_edit_content_url(self):
        return url_for('admin.edit_block_content',item_id=int(self.id))

    def _get_edit_url(self):
        return url_for('admin.edit_block',item_id=int(self.id))

    def _get_absolute_url(self):
        return url_for('admin.block_view',name=self.name)

    @property
    def line_count(self):
        try:
            rtn = len(self.content.split('\n'))
        except:
            rtn = 0
        return rtn

class Macro(BaseMixin,Model):
    __tablename__ = 'macros'

    name = Column(String(255),nullable=False)
    content = Column(Text)
    _args = Column(Text)
    
    def __init__(self,name='',content='',arguments=''):
        self.name = name
        self.content = content
        self.args = arguments

    @hybrid_property
    def args(self):
        return pickle.loads(self._args)

    @args.setter
    def args(self,args):
        if args:
            self._args = pickle.dumps(args)
        
    @property
    def head(self):
        start = '{% macro '
        mid = '%s' % self.name
        end = '('
        if self._args:
            arg_amount = len(self.args)
            for k,v in self.args:
                end += '%s=%s' % (k,v)
                if k != self.args[-1][0]:
                    end += ','
        end += ') %}'
        return start + mid + end

    @property
    def foot(self):
        return '{% endmacro %}'

    def __str__(self):
        return self.head +'\n'+\
               self.content +'\n'+\
               self.foot + '\n'



