import os
from sqlalchemy import desc
from flask import session, g, flash, redirect, url_for, request
from functools import wraps
from flask import url_for
from flask_cms.settings import BaseConfig

def get_files_of_type(ext):
    root = BaseConfig.ROOT_PATH
    count = 0
    rtn = {}
    counts = {}
    for dn,dl,fl in os.walk(os.path.abspath(root)):
        for f in fl:
            counts[count] = os.path.join(dn,f)
           
            if f.endswith(ext):
                with open(os.path.join(os.path.abspath(dn),f),'r') as fp:
                    if rtn.get("dn",False):
                        rtn[dn].append((f,fp.read(),count))                           
                    else:
                        rtn[dn] = [(f,fp.read(),count)]
            count += 1            
    return (rtn,counts)
        
    


class Pagination(object):
    _model = None
    _query = None
    _page_num = 1
    _objs = []
    _obj_page = []
    _per_page = BaseConfig.ADMIN_PER_PAGE
    _page_count = _per_page

    def __init__(self,model,page_num=None,query=None):
        if query is None:
            self._query = model.query.order_by(desc(model.id))
        else:
            self._query = query
        self._model = model
        self._page_num = int(page_num) or self._page_num
        self._objs = self._query.all()
        self.set_page(self._objs)

    def set_page(self,obj_list):
        s = ((int(self._per_page*self._page_num))-self._per_page)
        self._obj_page = []
        total = 0
        while total != self._per_page:
            for i in range(self._per_page):
                try:
                    self._obj_page.append(obj_list[s])
                except:
                    break
                finally:
                    s+=1 
                    total += 1
            break
        


    @property
    def has_next(self):
        return self._page_num != self._per_page*len(self._objs)

    @property
    def has_prev(self):
        return self._page_num != 1

    @property
    def next_link(self):
        if self.has_next:
            return url_for('admin.page_{}'.format(self._model.__name__.lower()),page_num=self.page_num+1)
        return '#'
        
    @property
    def prev_link(self):
        if self.has_prev:
            return url_for('admin.page_{}'.format(self._model.__name__.lower()),page_num=self._page_num-1)
        return '#'
        

def get_pk(obj):
    if 'id' in obj.__dict__:
        return obj.id
    raise IOError



def login_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['email'] = user.email

def logout_user(user):
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('email',None)

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return view(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('auth.login',next=request.url))
    return wrapper

def admin_required(view):
    @wraps(view)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            if User.get_by_id(session.get('user_id')).is_admin:
                return view(*args,**kwargs)
        flash('You need to login as an administrator to access that page.')
        return redirect(url_for('auth.login',next=request.url))
    return wrapper

