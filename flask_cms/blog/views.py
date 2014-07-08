from baseviews import BaseView
from flask import request, g
from blog import blog
from ext import db

admin_required = ''

class UnknownUser(object):
    email = ''
    username = ''
    id = 0

class BlogIndexView(BaseView):
    _template = 'index.html'

    def get(self):
        from .models import Article
        articles = Article.query.all()
        self._context['articles'] = articles
        return self.render()
        return self.redirect('member.blog_list',member_id=1)

blog.add_url_rule('/',view_func=BlogIndexView.as_view('index'))


class BlogAdminView(BaseView):
    _template = 'index.html'

    def get(self):
        return self.render()

blog.add_url_rule('/bloglist',view_func=BlogAdminView.as_view('member.admin_list',member_id=1))
blog.add_url_rule('/bloglist',view_func=BlogAdminView.as_view('list'))
from baseviews import BaseView
from member.forms import EditProfileForm
from member import member



def get_modal_forms(objs,db,**kwargs):
    from wtforms.ext.sqlalchemy.orm import model_form
    res = []
    for o in objs:
        res.append((o.id,model_form(o,db.session)))
    return res

class ModalEditView(BaseView):
    _template = 'add_blog.html'
    _form = None
    _context = {}

    def get(self,id):
        from .models import Article
        from .forms import AddContentModalForm
        a = Article.query.get_or_404(id)
        self._form = AddContentModalForm
        self._form._has_pagedown = True
        self._form_obj = a
        self._context['a'] = a
        return self.render()

    def post(self,id):
        from .models import Article
        a = Article.query.get(id)
        a.title = request.form.get('title')
        a.content = request.form.get('content')
        a.update()
        self._context['a'] = a
        return self.render()

blog.add_url_rule('/edit/<int:id>',view_func=ModalEditView.as_view('edit'))


class AddView(BaseView):
    _template = 'add_blog.html'
    _form = None
    _context = {}

    def get(self):
        from blog.forms import AddContentModalForm
        self._form = AddContentModalForm
        self._form._has_pagedown = True
        from .models import Article
        articles = Article.query.all()
        self._context['articles'] = articles
        return self.render()
    
    def post(self):
        from blog.forms import AddContentModalForm
        self._form = AddContentModalForm(request.form)
        from blog.models import Article
        a = Article()
        self._form.populate_obj(a)
        a.author = g.get('user',None) or UnknownUser()
        a.save()
        return self.redirect('blog.index')

blog.add_url_rule('/add',view_func=AddView.as_view('add'))


class MemberProfileView(BaseView):    
    _template = 'profile.html'
    _form = EditProfileForm
    _context = {}

    def get(self):
        return self.render()


    def post(self):
        return self.render()

class MemberArticleView(BaseView):
    _template = 'blog.html'
    _form = None
    _context = {}

    def get(self,blog_id=None,post_id=None,member_id=None):
        if blog_id is not None:
            pass
        if post_id is not None:
            from .models import Article
            a = Article.query.get(post_id)
            self._context['content'] = a
            self._context['type'] = 'article'
        self._context['nav_links'] = (('core.index', 'Home'), ('blog.blogs', 'Blog'), ('core.meet', 'Meet Us'), ('core.about', 'About'), ('core.contact', 'Contact'))
        self._context['member_id'] = member_id or 'unknown'
        self._context['nav_title'] = 'My Blog'
        return self.render()

blog.add_url_rule('/blogs',view_func=MemberArticleView.as_view('blogs'))
blog.add_url_rule('/blog/<blog_id>',view_func=MemberArticleView.as_view('post_list'))
blog.add_url_rule('/post/<post_id>',view_func=MemberArticleView.as_view('post_detail'))
blog.add_url_rule('/post/<post_id>/edit',view_func=MemberArticleView.as_view('post_edit'))
blog.add_url_rule('/blog/<blog_id>/edit',view_func=MemberArticleView.as_view('blog_edit'))

'''
#private
def article_update(id, slug):
    article = Article.find_by_id(id)
    if not article:
        return HTTPNotFound(404)
    form = ArticleUpdateForm(request.form, article)
    person = Person.query.filter_by(email=session['email']).first()
    name = person.firstname
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=form, name=name)

#private
@app.route('/category/create', methods=['GET', 'POST'])
def category():
    form = CategoryCreateForm()
    category = Category()
    person = Person.query.filter_by(email=session['email']).first()
    name = person.firstname
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('dashboard', name=name))
    return render_template('cat_create.html', form=form)


#private
@app.route('/dashboard/<name>')
def dashboard(name):
    if 'email' not in session:
        return redirect(url_for('index'))
    person = Person.query.filter_by(email=session['email']).first()
    if name == person.firstname:
        articles = Article.find_by_author(name)
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        return render_template('dashboard.html', articles=articles, person=person, name=name)
    return redirect(url_for('index'))

#private
@app.route('/article/<int:id>/<slug>/delete', methods=['GET','POST'])
def delete(id, slug):
    article = Article.find_by_id(id)
    person = Person.query.filter_by(email=session['email']).first()
    '''
