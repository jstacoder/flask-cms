import os
from settings import BaseConfig

root = BaseConfig.ROOT_PATH


templates = os.listdir(os.path.join(root,'page','templates','cms'))

def get_page_templates():
    return templates
