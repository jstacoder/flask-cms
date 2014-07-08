from flask import session, g, flash, redirect, url_for, request
from functools import wraps


def login_user(user):
    if 'email' in session:
        session.pop('email')
    session['email'] = user.email
    session['user_id'] = user.id

def logout_user(user):
    session.pop('email')
    session.pop('user_id')
    return redirect(url_for('core.index'))

def login_required(view):
    @wraps(view)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            if 'email' in session:
                return view(*args,**kwargs)
        flash('You need to login as an administrator to access that page.')
        return redirect(url_for('auth.login',next=request.url))
    return wrapper

