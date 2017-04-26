from flask_xxl.basemodels import BaseMixin
import jinja2 
import datetime
import os
from flask import url_for, Markup
from flask.templating import render_template_string as render_str
import pickle
from sqlalchemy.ext.hybrid import hybrid_property
from flask_xxl.main import AppFactory
from flask_cms.settings import DevelopmentConfig
from sqlalchemy import Integer,Column,Table,ForeignKey,Boolean,DateTime,Text,String,Enum
from sqlalchemy.orm import relationship,backref
app = AppFactory(DevelopmentConfig).get_app(__name__)

root = DevelopmentConfig.ROOT_PATH

class Super(super):
    def __getattr__(self,attr):
        return self.__self__.__getattr__(attr)


pages_macros = Table('pages_macros',BaseMixin.metadata,
    Column('page_id',Integer,ForeignKey('pages.id')),
    Column('macro_id',Integer,ForeignKey('macros.id')),
    extend_existing=True
)

pages_template_blocks = Table('pages_template_blocks',BaseMixin.metadata,
    Column('page_id',Integer,ForeignKey('pages.id')),
    Column('template_block_id',Integer,ForeignKey('template_blocks.id')),
    extend_existing=True
)

class Template(BaseMixin):

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
        return len( Template(self._head + self.body[:]).blocks)

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

    @property
    def filename(self):
        return "{}.html".format(self.name if self.name else self.id)

class Block(BaseMixin):

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

class Macro(BaseMixin):
    MACRO_FILE = os.path.join(os.path.abspath(root),'macros.html')

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

    @property
    def import_statement(self):
        return self._generate_import()

    def _generate_import(self):
        start = '{% from "'
        end = ' %}'
        mid = '%s" import %s' % (self.MACRO_FILE,self.name)
        return start + mid + end

    @staticmethod
    def _generate_macro_file(names=None):
        res = ''
        if names is None:
            macros = Macro.query.all()
        else:
            macros = [Macro.query.filter(Macro.name==x).all()[0] for x in names]
        for macro in macros:
            res += str(macro)
            res += '\n'
        try:
            with open(Macro.MACRO_FILE,'w') as fp:
                fp.write(res)
        except IOError, e:
            return False
        return True
                

class Button(BaseMixin):

    name = Column(String(255),nullable=False,unique=True)
    type = Column(String(255),nullable=False,default='button')
    color = Column(Enum('blue','grey','light-blue','yellow','green','red',name='color'),default='grey',nullable=False)
    size = Column(Enum('XL','L','M','S','XS',name='size'),default='M',nullable=False)
    text = Column(String(255))
    icon = Column(String(255))
    icon_library = Column(String(255))
    _endpoint = Column(String(255))
    is_link = Column(Boolean,default=False) 
    icon_id = Column(Integer,ForeignKey('font_icons.id'))
    _icon = relationship('flask_cms.admin.models.FontIcon')

    @hybrid_property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self,endpoint):
        self._endpoint = endpoint
        if endpoint:
            self.is_link = True
        else:
            self.is_link = False

    def _get_absolute_url(self):
        return url_for('admin.view_button',item_id=self.id)

    def _get_edit_url(self):
        return url_for('admin.view_button',item_id=self.id)

    @classmethod
    def get_id_by_name(cls,name):
        b = cls.query.filter(cls.name==name).first()
        if b:
            rtn = b.id
        else:
            rtn = 0
        return rtn
        

class StaticBlock(BaseMixin):

    name = Column(String(255),nullable=False)
    block_id = Column(String(255),nullable=False,unique=True,default=name)
    content = Column(Text)

    @hybrid_property
    def _blocks(self):
        blocks = lambda: self.session.query(self).all()
        return {x.block_id:x for x in blocks}

    @hybrid_property
    def _block_names(self):
        blocks = lambda: self.session.query(self).all()
        return {x.name:x for x in blocks}
    
    @property
    def title(self):
        return self.name

    @staticmethod
    def get_by_block_id(block_id):
        return StaticBlock.query.filter(StaticBlock.block_id==block_id).first()
    
    def render(self,**kwargs):
        return Markup(render_str(self._get_macro_header() + '\n' + self.content,**kwargs))

    def __str__(self):
        return 'static_block: {}<{}>'.format(
                self.name,self.block_id)
    
    def __call__(self,**kwargs):
        return self.render(**kwargs)

    def __repr__(self):
        return self.content

    def _get_macro_header(self):
        return open(Macro.MACRO_FILE,'r').read()


class TemplateBlock(BaseMixin):
    block_id = Column(String(255),unique=True,nullable=False)
    content = Column(Text,default='')

    @property
    def name(self):
        return self.block_id

    def __str__(self):
        return self.render()

    def render(self):
        return self.content



class Page(BaseMixin):
    _use_base_template = None

    name = Column(String(255))
    description = Column(Text)
    template_id = Column(Integer,ForeignKey('templates.id'))
    template = relationship(Template,backref=backref(
                'pages',lazy='dynamic'))
    slug = Column(String(255))
    title = Column(String(255))
    add_to_nav = Column(Boolean,default=False)
    add_left_sidebar = Column(Boolean,default=False)
    add_right_sidebar = Column(Boolean,default=False)
    date_added = Column(DateTime,default=datetime.datetime)
    visible = Column(Boolean,default=False)
    meta_title = Column(String(255))
    added_by = relationship('flask_cms.auth.models.User')
    user_id = Column(Integer,ForeignKey('users.id'))
    short_url = Column(String(255))
    macros = relationship(Macro,secondary='pages_macros',
                            backref=backref('pages',lazy='dynamic'),
                            lazy='dynamic')
    _blocks = relationship(TemplateBlock,secondary='pages_template_blocks',
                            backref=backref('pages'),lazy='dynamic')

    content = Column(Text)

    def __repr__(self):
        if self.name is None:
            rtn = '<Page: Unnamed | {}'.format(self.line_count)
        else:
            rtn = '<Page: {} | {} lines'.format(self.name,self.line_count)
        return rtn

    @property
    def use_base_template(self):
        return bool(self.template) if self._use_base_template is None else self._use_base_template

    @use_base_template.setter
    def use_base_template(self, val):
         self._use_base_template = val

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
        return self._template.blocks.count()

    @property
    def blocks(self):
        return self._template.blocks.keys()


    def get_block(self,block):
        return self._template.blocks[block]
        return str(self._blocks.get_by_name(block))
    
    @property
    def _template(self):
        class template(object):
            def __init__(self):
                self.blocks = {'blocka':'','blockb':'','blockc':'x','blockd':''}
        return template()
