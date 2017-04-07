from flask_xxl.basemodels import BaseMixin
import sqlalchemy as sa


class Menu(BaseMixin):
    name = sa.Column(sa.String(255))


