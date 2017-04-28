

def lazy_import(module, *args):
    rtn = []
    for itm in args:
        rtn.append(getattr(__import__(module,{},{},fromlist=[]), itm))
    return rtn[0] if len(rtn) == 1 else rtn
