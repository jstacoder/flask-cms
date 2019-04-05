import os
from setuptools import setup, findall

setup(
    name='flask-cms',
    packages=['flask_cms'],
    package_data={'':findall('flask_cms')},
    version='0.0.4',
    install_requires=open(os.path.join(os.getcwd(), 'flask_cms', 'requirements.txt'),'r').readlines(),
)
