from flask_xxl.basemodels import BaseMixin
import sqlalchemy as sa

class File:
    __table_args__ = {'abstract':True}
    __abstract__ = True

    name = sa.Column(sa.String(255),nullable=False)
    parent_id = sa.Column(sa.Integer,sa.ForeignKey('directories.id'))
    parent = sa.orm.relationship('Directory',backref=sa.orm.backref(
                        'files',lazy='dynamic'))
    full_path = sa.Column(sa.String(255),nullable=False,unique=True)

class Directory(BaseMixin):

    name = sa.Column(sa.String(255),nullable=False)
    full_path = sa.Column(sa.String(255),nullable=False,unique=True)

class TemplateFile(File,BaseMixin):
    pass

class CodeFile(File,BaseMixin):
    pass


    



