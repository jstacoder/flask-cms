from flask_xxl.basemodels import BaseMixin
from LoginUtils import check_password, encrypt_password
from sqlalchemy import Column,String,Integer,ForeignKey,Boolean,Text
from sqlalchemy.orm import relationship,backref


class Setting(BaseMixin):

    name = Column(String(255),nullable=False,unique=True)
    setting_type_id = Column(Integer,ForeignKey('types.id'))
    setting_type = relationship('Type',backref=backref(
        'settings',lazy='dynamic'))
    default = Column(String(255))
    value = Column(String(255))

    @property
    def widget(self):
        if self.type:
            return self.type.widgets
        else:
            return ''

class Type(BaseMixin):

    name = Column(String(255),nullable=False)
    widgets = relationship('Widget',backref=backref(
        'type'),lazy='dynamic')
    html = Column(Text)
    field_type = Column(String(255))
    required = Column(Boolean,default=False)
    data_type = Column(String(255))

    def __repr__(self):
        return self.name or ''

class Widget(BaseMixin):
   

    name = Column(String(255),nullable=False)
    title = Column(String(255))
    content = Column(Text,nullable=False)
    type_id = Column(Integer,ForeignKey('types.id'))

    def __repr__(self):
        return self.name


class AdminTab(BaseMixin):
    

    name = Column(String(255),nullable=False)
    tab_id = Column(String(50),nullable=False)
    tab_title = Column(String(255))
    content = Column(Text)

    def __str__(self):
        return self.content or ''

    @staticmethod
    def get_tab_links():
        rtn = []
        for panel in AdminTab.query.all():
            rtn.append((panel.name,panel.tab_id))
        return rtn
    
    
class FontIcon(BaseMixin):
   
    name = Column(String(255),nullable=False)
    library_id = Column(Integer,ForeignKey('font_icon_librarys.id'))
    library = relationship('FontIconLibrary',backref=backref(
                'font_icons',lazy='dynamic'))

    #__table_args__ = (UniqueConstraint(library,name,name='_library_font_icon'),)
    
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return '<span class="{0} {0}-{1}"></span>'.format(self.library.name,self.name)

class FontIconLibrary(BaseMixin):   
    __tablename__ = 'font_icon_librarys'

    name = Column(String(255),unique=True)
    call_string = Column(String(255),unique=True)

    




    
