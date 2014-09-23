from main.baseviews import BaseView
from slugify import slugify
from member.forms import EditProfileForm
from member import member
from flask import request, g,url_for,session
from blog import blog
from ext import db

admin_required = ''

class UnknownUser(object):
    email = ''
    username = ''
    id = 0

class BlogIndexView(BaseView):
    _template = 'two_column_right.html'

    def get(self):
        from .models import Article
        from .models import Tag
        tags = Tag.query.all()
        articles = Article.query.all()
        self._context['articles'] = articles
        self._context['tags'] = tags
        return self.render()



class BlogAdminView(BaseView):
    _template = 'index.html'

    def get(self):
        return self.render()


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
        from .models import Article,Tag
        a = Article.query.get(id)
        a.title = request.form.get('title')
        a.content = request.form.get('content')
        tags = request.form.get('tags','')
        tags = tags.split(',')
        Tag.update_tags(tags)
        a.update()
        self._context['a'] = a
        return self.render()



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
        from auth.models import User
        self._form = AddContentModalForm(request.form)
        from blog.models import Article
        a = Article()
        self._form.populate_obj(a)
        a.author = User.query.filter(User.email==session.get('email',None)).first()
        a.save()
        return self.redirect('blog.index')



class MemberProfileView(BaseView):
    _template = 'profile.html'
    _form = EditProfileForm
    _context = {}

    def get(self):
        return self.render()


    def post(self):
        return self.render()

class MemberArticleView(BaseView):
    _template = 'blog_home.html'
    _form = None
    _context = {
            'body_style':'margin-top:0px;',
            'wide':False,

    }

    def get(self,blog_id=None,post_id=None,member_id=None):
        from page.widgets import TagWidget
        if blog_id is not None:
            pass
        if post_id is not None:
            from .models import Article
            a = Article.query.get(post_id)
            self._context['content'] = a
            self._context['type'] = 'article'
        self._context['sidebar_title'] = 'menu'
        self._context['sidebar_links'] = (
                                    (url_for('core.index'),'Home'),
                                    (url_for('blog.blogs'),'Blog'),
                                    (url_for('core.meet'),'meet us'),
                                        )
        self._context['nav_links'] = (
                                    ('core.index', 'Home'),
                                    ('blog.blogs', 'Blog'),
                                    ('core.meet', 'Meet Us'),
                                    ('core.about', 'About'),
                                    ('core.contact', 'Contact')
                                    )
        self._context['member_id'] = member_id or 'unknown'
        self._context['nav_title'] = 'My Blog'
        self._context['sidebar_widgets'] = [TagWidget()]
        g.nav_id = 'clean'
        return self.render()


class TagListView(BaseView):
    _template = 'taglist.html'
    _context = {}

    def get():
        return self.render()

class FrontBlogView(BaseView):
    _template = 'front_blog_list.html'
    _context = {}

    def get(self):
        from .models import Blog
        self._context['blogs'] = Blog.get_by_author_id(session.get('user_id',None))
        return self.render()

class AjaxAddBlogView(BaseView):

    def get(self):
        from .models import Blog, Article, Tag, Category
        data = dict(
            date_added=request.args.get('date_added',None),
            date_end=request.args.get('date_end',None),
            name=request.args.get('name',None),
            description=request.args.get('description',None),
            slug=request.args.get('slug',None),
            short_url=request.args.get('short_url',None),
            title=request.args.get('title',None),
            add_to_nav=request.args.get('add_to_nav',None),
            add_sidebar=request.args.get('add_sidebar',None),
            visible=request.args.get('visible',None),
            meta_title=request.args.get('meta_title',None),
            content=request.args.get('content',None),
            template=request.args.get('template',None),
            category=request.args.get('category',None),
            tags=request.args.get('tags',None),
            use_base_template=request.args.get('use_base_template',None),
        )
        blog = Blog.get_current_blog()
        post = Article.query.filter(Article.name==data['name'])\
                            .filter(Article.blog==blog)\
                            .first()
        if post is not None:
            res = 0
        else:
            tags = [x.name for x in Tag.query.all()]
            new_tags = []
            for tag in data['tags']:
                if not tag in tags:
                    t = Tag()
                    t.name = tag
                    new_tags.append(t.save())
            new_tags = new_tags + tags
            post = Article()
            post.tags = new_tags
            post.name = data.get('name')
            post.date_added = data.get('date_added')            
            post.description = data.get('description',None)
            post.slug = data.get('slug',None)
            post.url = data.get('short_url',None)
            post.title = data.get('title',None)            
            post.visible = data.get('visible',None)
            post.meta_title = data.get('meta_title',None)
            post.content = data.get('content',None)
            post.category = data.get('category',None)
            post.save()
            res = 1
        return jsonify(result=res,content=data['content'])


class BlogListView(BaseView):
    _template = 'blog_list.html'
    _context = {
            'body_style':'',
    }

    def get(self):
        from .models import Blog
        blogs = Blog.query.all()
        self._context['blogs'] = blogs
        if len(blogs) == 1:
            blog = blogs[0]
            return self.redirect('blog.list_posts',item_id=blog.id)
        return self.render()

class PostListView(BaseView):
    _template = 'post_list.html'
    _context = {
            'body_style':'',
    }

    def get(self,item_id):
        from .models import Blog
        blog = Blog.get_by_id(item_id)
        if blog is None:
            self.flash('Error: No blog found with id: {}'.format(item_id))
            return self.redirect('core.index')
        self._context['blog'] = blog
        self._context['posts'] = blog.posts 
        return self.render()

class SinglePostView(BaseView):
    _template = 'post.html'
    _context = {
            'body_style':'',
    }

    def get(self,item_id):
        from .models import Post
        post = Post.get_by_id(item_id)
        if post is None:
            self.flash('Error: No post found with id: {}'.format(item_id))
            return self.redirect('core.index')
        self._context['post'] = post
        return self.render()

class AddPostView(BaseView):
    _template = 'add_post.html'
    _context = {'wide':True}

    def get(self):
        from .forms import AddPostForm
        self._form = AddPostForm

        return self.render()

    def post(self):
        from .forms import AddPostForm
        self._form = AddPostForm(request.form)
        if self._form.validate():
            from .models import Post,Blog,Category,Tag
            post = Post.query.filter(Post.name==self._form.name.data).first()
            if post is None:
                blog = Blog.query.all()[0]
                post = Post()
                post.name = self._form.name.data
                post.content = self._form.content.data
                post.category = Category.get_by_name(self._form.category.data)
                post.slug = slugify(unicode(post.name))
                #post.tags = [t for t in self._form.tags.data if not t in [tag.name for tag in Tag.query.all()]]
                post.author_id = g.get('user_id',None)
                if self._form.excerpt_length.data and self._form.excerpt_length.data > 0: 
                    post.excerpt_length = self._form.excerpt_length.data
                post.blog = blog
                post.save()
                self.flash('add a new post to {}'.format(blog.name))
            else:
                self.flash('A post exists with that name')
        else:
            self.flash('form validation error')
        return self.redirect('core.index')
            


        



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
