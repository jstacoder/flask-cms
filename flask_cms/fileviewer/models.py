from main.basemodels import BaseMixin
from ext import db

class File:
    __table_args__ = {'abstract':True}
    __abstract__ = True

    name = db.Column(db.String(255),nullable=False)
    parent_id = db.Column(db.Integer,db.ForeignKey('directories.id'))
    parent = db.relationship('Directory',backref=db.backref(
                        'files',lazy='dynamic'))
    full_path = db.Column(db.String(255),nullable=False,unique=True)



class Directory(BaseMixin,db.Model):
    __tablename__ = 'directories'

    name = db.Column(db.String(255),nullable=False)
    full_path = db.Column(db.String(255),nullable=False,unique=True)


class TemplateFile(File,BaseMixin,db.Model):
    __tablename__ = 'template_files'

class CodeFile(File,BaseMixin,db.Model):
    __tablename__ = 'code_files'


    



