import os

def get_files(dirname,exclude):
    data = os.walk(dirname)
    rtn = {}
    for dn,dl,fl in data:
        for name in exclude:
            if name in dn:
                pass
            else:
                dn = os.path.realpath(dn)
                rtn[dn] = fl
    return rtn

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_files(os.getcwd(),exclude=['static','ckeditor','.git']),indent=2)
