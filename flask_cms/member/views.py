from flask_xxl.baseviews import BaseView
from flask_cms.member.forms import EditProfileForm
from flask_cms.member import member
from flask import abort







class MemberProfileView(BaseView):    
    _template = 'profile.html'
    _context = {}

    def get(self,member_id):
        from auth.models import User
        user = User.query.get_or_404(member_id)
        if user is not None:
            self._context['user'] = user
        else:
            self.flash('No user with id {} found'.format(member_id))
        return self.render()


    def post(self):
        return self.render()

class EditProfileView(BaseView):
    _template = 'profile.html'
    _form = EditProfileForm
    _context = {}

    def get(self,member_id):
        if session.get('user_id') != member_id:
            return abort(403)
        from auth.models import User
        self._context['user'] = User.query.get_or_404(member_id)
        self._context['member'] = Member.query.get(member_id)
        self._form_args = {
                'last_name':user.last_name,
                'phone_number':member.phone_number,
                'birth_date':member.birth_date,
                'first_name':user.first_name,
                'email':user.email,
        }
        return self.render()

    

class MemberArticleView(BaseView):
    _template = 'blog.html'
    _form = None
    _context = {}

    def get(self,blog_id=None,post_id=None,member_id=None):
        self._context['nav_links'] = (('core.index', 'Home'), ('blog.blogs', 'Blog'), ('core.meet', 'Meet Us'), ('core.about', 'About'), ('core.contact', 'Contact'))
        self._context['member_id'] = member_id or 'unknown'
        self._context['nav_title'] = 'My Blog'
        return self.render()


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
