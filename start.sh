#!/root/anaconda/bin/python
import os
import sys
import sqlalchemy_utils as squ
from app.models import *

URL = 'mysql+pymysql://test:test@174.140.227.137/test_new' 
os.environ['DATABASE_URL'] = URL

def setup_db(reset=False):
    if reset:
        squ.drop_database(URL)
    if not squ.database_exists(URL):
        squ.create_database(URL)
    return reset


def main():
    from app import db
    reset = len(sys.argv) > 1
    if setup_db(reset):
        os.system('python ./manage3.py init')
    os.system('python ./manage.py runserver --host="0.0.0.0" --port=8082')

if __name__ == "__main__":
    main()
