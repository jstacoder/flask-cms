# coding: utf-8
def make_icon_list_file(icons):
    f = open('tmp.py','w')
    fmt = '    "{}",'
    start = '[\n'
    end  = ']\n'
    f.write(start)
    for icon in icons:
        f.write(fmt.format(icon))
        f.write('\n')
    f.write(end)
    f.close()
    