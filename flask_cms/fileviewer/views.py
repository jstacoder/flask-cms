from main.baseviews import BaseView
from flask import request
from forms import CodeForm
from settings import DevelopmentConfig
import os.path as op
import os

root = DevelopmentConfig.ROOT_PATH

IGNORE_EXTENSIONS = ['pyc','swp']

def save_file(name,content):
    old = open(name,'r').read()
    if old.strip() != content.strip():
        with open(name,'w') as f:
            f.write(content)
        return True
    return False

def get_editor_mode(name):
    modes = {
        'py':'python',
        'html':'jinja2',
        'php':'php',
        'js':'javascript',
    }
    return modes[name.split('.')[-1]]


def filter_files(files):
    rtn = []
    for f in files:
        end = f[-3:]
        if end in IGNORE_EXTENSIONS:
            pass
        else:
            #files.pop(files.index(f))
            rtn.append((op.basename(f),op.relpath(f)))
    return rtn


def split_files_and_dirs(dirname):
    contents = os.listdir(dirname)
    files,dirs = [],[]
    for itm in contents:
        tmp = op.join(dirname,itm)
        if op.isdir(tmp):
            dirs.append(itm)
        else:            
            files.append(op.join(dirname,itm))
    return filter_files(files),dirs



class FileView(BaseView):
    _template = 'view_files.html'
    _context = {'files':[],'dirs':[],'file_content':''}

    def get(self):
        item_name = request.args.get('item_name',None)
        if item_name is None:
            # get inital dir and file list to display
            d = root
            self._context['files'],self._context['dirs'] = split_files_and_dirs(d)            
        else:
            # find out if its a dir or a file
            is_file = False
            if not op.isdir(item_name):
                is_file = True
            if not is_file:
                # is dir, list files
                self._context['files'],self._context['dirs'] = split_files_and_dirs(item_name)            
                self._context['current_dir'] = item_name
            else:
                # is file, edit
                self._template = 'file_editor.html'
                self._context['file_content'] = open(item_name,'r').read()
                self._context['file_name'] = item_name
                self._form_args = {'file_name':item_name}
                self._context['editor_mode'] = get_editor_mode(item_name)
                self._form = CodeForm
        return self.render()


    def post(self):
        content = request.form.get('content')
        name = request.form.get('file_name')
        self._context['file_name'] = name
        self._template = 'save_file.html'
        self._context['content'] = content
        self._context['exists'] = op.exists(name) and op.isfile(name)
        if save_file(name,content):
            self.flash('successfully saved {}'.format(name))
        return self.redirect('.view_files')


