from main.baseviews import BaseView
from member.forms import EditProfileForm
from member import member




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
