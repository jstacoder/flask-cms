import os

print os.path.realpath(os.getcwd())
print os.path.realpath(os.path.dirname(__file__))
