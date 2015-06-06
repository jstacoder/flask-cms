from setuptools import setup

setup(
    name='flask-cms',
    packages=['flask_cms'],
    version='0.0.1',
    install_requires=open('flask_cms/requirements.txt','r').readlines(),
)
