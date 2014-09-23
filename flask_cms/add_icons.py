import icon.icons as ii
import os


libs = []



COMPLETED_FILE = os.path.join(os.path.expanduser('~'),'.completed_fcms')

def get_libs():
    for lib in dir(ii):
        if not lib.startswith('_'):
            libs.append((lib,getattr(ii,lib),))
    return libs

def make_completed_file():
    if not check_completed_file():
        os.system('touch {}'.format(COMPLETED_FILE))

def check_completed_file():
    return os.path.exists(COMPLETED_FILE)

def main():
    from app import app
    app.test_request_context().push()
    from admin.models import FontIcon,FontIconLibrary
    from imports import (
            Widget,Article,Page,User,Setting,
            Type,Template,Tag,Role,Category,Block,
            Profile,ContactMessage,Blog,Macro,Button,
            StaticBlock,TemplateBlock,AdminTab,Post,FontIcon,
            FontIconLibrary
            )
    for lib,icons in get_libs():
        l = FontIconLibrary()
        l.name = lib
        for icon in icons:
            i = FontIcon()
            i.name = icon
            i.library = l
        try:
            l.save()
        except IntegrityError:
            pass

    make_completed_file()

if __name__ == "__main__":
    if not check_completed_file():
        main()









