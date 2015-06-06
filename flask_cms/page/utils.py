import os
from flask_cms.settings import BaseConfig

root = BaseConfig.ROOT_PATH


templates = os.listdir(os.path.join(root,'page','templates'))

def get_page_templates():
    return templates
