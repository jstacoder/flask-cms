from basemodels import BaseMixin
from datetime import datetime
from ext import db
from flask import url_for

for attr in dir(db):
    globals()[attr] = getattr(db,attr)

class Page(BaseMixin,Model):
    __tablename__ = 'pages'

    name = Column(String(255))
    description = Column(Text)
    template_id = Column(Integer,ForeignKey('templates.id'))
    template = relationship('Template',backref=backref(
                'pages',lazy='dynamic'))
    blocks = relationship('Block',secondary='pages_blocks',
            backref=backref('pages',lazy='dynamic'),lazy='dynamic')
    slug = Column(String(255))
    title = Column(String(255))
    add_to_nav = Column(Boolean,default=False)
    #date_added = Column(DateTime,default=datetime.datetime)
    visible = Column(Boolean,default=False)
    meta_title = Column(String(255))
    content = Column(Text)
    use_base_template = Column(Boolean,default=True)
    added_by = relationship('User',backref=backref(
        'pages',lazy='dynamic'))
    user_id = Column(Integer,ForeignKey('users.id'))

    def __repr__(self):
        if self.name is None:
            rtn = '<Page: Unnamed | {}'.format(self.line_count)
        else:
            rtn = '<Page: {} | {} lines'.format(self.name,self.line_count)
        return rtn
       

    @property
    def add_to_sidebar(self):
        return self.add_to_nav

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
        return self.blocks.count()


class Template(BaseMixin,Model):
    __tablename__ = 'templates'
    
    name = Column(String(255))
    body = Column(UnicodeText)
    filename = Column(String(255))
    blocks = relationship('Block',secondary='templates_blocks',
                            backref=backref(
                            'templates',lazy='dynamic'),
                            lazy='dynamic')

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
        return self.body
        
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

    @property
    def sections(self):
        return ['a','b','c']

    def process_blocks(self,blocks):
        for b in blocks:
            if b.section in self.sections:
                self.add_block(b)

    def add_block(self,block):
        self._temp = self.body[:] % block
     

class Block(BaseMixin,Model):
    __tablename__ = 'blocks'
    
    name = Column(String(255))
    content = Column(String(1000))
    description = Column(String(255))
    
    def __str__(self):
        s = self.content.split('\n')
        return '<br />'.join(map(str,s))

    def __repr__(self):
        if self.name is None:
            rtn = '<Block: Unnamed | {} lines'.format(self.line_count)
        else:
            rtn = '<block: {} | {} lines'.format(self.name,self.line_count)
        return rtn


    @property
    def section(self):
        return 'a'

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



pages_blocks = Table('pages_blocks',metadata,
        Column('page_id',Integer,ForeignKey('pages.id')),
        Column('block_id',Integer,ForeignKey('blocks.id')),
)

templates_blocks = Table('templates_blocks',metadata,
        Column('template_id',Integer,ForeignKey('templates.id')),
        Column('block_id',Integer,ForeignKey('blocks.id')),
)
