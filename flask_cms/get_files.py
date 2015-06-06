import os
from pprint import pprint

def get_files(dirname,exclude):
    data = os.walk(dirname)
    rtn = {}
    for dn,dl,fl in data:
        if not any(filter(lambda x: (x in dn or any(filter(lambda f:x in f ,fl))),exclude)):
            dn = os.path.realpath(dn)
            rtn[dn] = fl
    return rtn

def get_templates(display=False):
    result = get_files(os.getcwd(),exclude=['static','ckeditor','.git','.swp','.mako','.py'])
    return display and print_res(result) or result

def get_pyfiles(display=False):
    result = get_files(os.getcwd(),exclude=['static','ckeditor','.git','.swp','.mako','.html'])
    return display and print_res(result) or result

def print_res(data):
    pprint(data,indent=2)

if __name__ == "__main__":
    pprint(get_files(os.getcwd(),exclude=['static','ckeditor','.git','.swp','.mako']),indent=2)
