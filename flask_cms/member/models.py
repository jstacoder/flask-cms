from flask_xxl.basemodels import BaseMixin
import datetime
from sqlalchemy import Column,String,Date,Integer,ForeignKey
from sqlalchemy.orm import relationship,backref

class Profile(BaseMixin):

    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(20))
    date_added = Column(Date,default=datetime.datetime)
    visits = Column(Integer,default=1)
    user_id = Column(Integer,ForeignKey('users.id'))
    birth_date = Column(Date)
    user = relationship('flask_cms.auth.models.User',backref=backref(
                'profile',uselist=False))



