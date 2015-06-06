import os
from pprint import pprint


def check_dir(name_a,name_b):
    return name_a in name_b

def check_ext(name,ext):
    return name.endswith(ext)

def get_files(dirname,exclude=None):
    pre_exclude = ['venv','.swp','.pyc']
    exclude = exclude and (exclude + pre_exclude) or pre_exclude
    data = os.walk(dirname)
    rtn = {}
    for dn,dl,fl in data:
        if not any(filter(lambda x: check_dir(x,dn), exclude)):
        #if not any(filter(lambda x: (x in dn or any(filter(lambda f:x in f ,fl))),exclude)):
            dn = os.path.realpath(dn)
            rtn[dn] = [ f for f in fl if not any(filter(lambda x: f.endswith(x),exclude))]
    return rtn

def get_templates(display=True):
    result = get_files(os.getcwd(),exclude=['static','ckeditor','.git','.swp','.mako','.py'])
    return display and print_res(result) or result

def get_pyfiles(display=True):
    result = get_files(os.getcwd(),exclude=['static','ckeditor','.git','.swp','.mako','.html'])
    return display and print_res(result) or result

def print_res(data):
    pprint(data,indent=2)
    return True

if __name__ == "__main__":
    pprint(get_files(os.getcwd(),exclude=['static','ckeditor','.git','.mako']),indent=2)
