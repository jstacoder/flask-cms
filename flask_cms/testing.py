#-*- coding: utf-8 -*-

"""
    testing.py
    ~~~~~~~
    TestCase for testing
    :license: BSD3
"""

from flask.ext.testing import TestCase
#from blog import Blog,Tag,Post
#from page import Page,Template,Block,Subject
from flask_xxl.main import AppFactory
from settings import TestingConfig
from sqlalchemy import MetaData,create_engine,orm

meta = MetaData()
engine = create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI,echo=True)
meta.bind = engine
meta.reflect()
session = orm.scoped_session(orm.sessionmaker(bind=engine))

class DB(object):
    def __init__(self,engine,session,meta):
        self.engine = engine
        self.session = session
        self.metadata = meta


class TC(TestCase):

    def create_app(self):
        return AppFactory(TestingConfig).get_app(__name__)

    def setUp(self):
        self.app = self.create_app()
        
        self.db = DB(engine,session,meta)
        import sqlalchemy_utils as squ
        if squ.database_exists(self.db.engine.url):
            squ.drop_database(self.db.engine.url)
        squ.create_database(self.db.engine.url)
        meta.bind = self.db.engine
        meta.create_all()

    def tearDown(self):
        self.db.session.remove()
        meta.drop_all()


    def assertContains(self, response, text, count=None,
                       status_code=200, msg_prefix=''):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """

        if msg_prefix:
            msg_prefix += ": "

        self.assertEqual(response.status_code, status_code,
            msg_prefix + "Couldn't retrieve content: Response code was %d"
                         " (expected %d)" % (response.status_code, status_code))

        real_count = response.data.count(text)
        if count is not None:
            self.assertEqual(real_count, count,
                msg_prefix + "Found %d instances of '%s' in response"
                             " (expected %d)" % (real_count, text, count))
        else:
            self.assertTrue(real_count != 0,
                    msg_prefix + "Couldn't find '%s' in response" % text)
