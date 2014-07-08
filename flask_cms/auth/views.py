from flask import session
from baseviews import BaseView
from auth import auth
from auth.forms import UserLoginForm, UserSignupForm
from auth.utils import login_user, logout_user, login_required


class AuthLoginView(BaseView):
    _template = 'auth_login.html'
    _form = UserLoginForm
    _context = {}

    def get(self):        
        return self.render()


    def post(self):
        form = self._form()
        from auth.models import User
        if form.validate():
            email = form.email.data
            pw = form.password.data
            remember = form.keep_me_logged_in.data
            u = User.get_by_email(email)
            if u is not None:
                if u.check_password(pw):
                    login_user(u)
                    return self.redirect('core.index')
                else:
                    flash('incorrect password')
            else:
                flash('user does not exist')
                return self.redirect('auth.signup')
        return self.render()

class AuthSignupView(BaseView):
    _template = 'register.html'
    _form = UserSignupForm
    _context = {}
    
    def get(self):
        return self.render()

    def post(self):
        from auth.models import User
        form = self._form()
        if form.validate():
            email = form.email.data
            pw = form.password.data
            u = User(email=email)
            u.password = pw
            login_user(u)
            self.flash("Thank you for signing up {}".format(email))
            return self.redirect('core.index')
        return self.redirect('auth.signup')



auth.add_url_rule('',view_func=AuthLoginView.as_view('admin_list'))
auth.add_url_rule('/login',view_func=AuthLoginView.as_view('login'))
auth.add_url_rule('/register',view_func=AuthSignupView.as_view('signup'))

class AuthLogoutView(BaseView):


    def get(self):
        from auth.models import User
        from auth.utils import logout_user
        if 'user_id' in session:
            user = User.get_by_id(session['user_id'])
            logout_user(user)
        return self.redirect('core.index')

auth.add_url_rule('/logout',view_func=AuthLogoutView.as_view('logout'))
