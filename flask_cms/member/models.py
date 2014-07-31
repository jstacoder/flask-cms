from main.basemodels import BaseMixin
import datetime
from ext import db

#import sqlalchemy to global namespace
for attr in dir(db):
    if not attr.startswith('_'):
        globals()[attr] = getattr(db,attr)


class Profile(BaseMixin,Model):
    __tablename__ = 'profiles'

    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(20))
    date_added = Column(Date,default=datetime.datetime)
    visits = Column(Integer,default=1)
    user_id = Column(Integer,ForeignKey('users.id'))
    birth_date = Column(Date)
    user = relationship('User',backref=backref(
                'profile',uselist=False))



