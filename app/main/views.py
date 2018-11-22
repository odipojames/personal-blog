from flask import render_template, redirect,url_for,abort
from flask_login import login_required, current_user
from . import main
from .forms import BlogForm, CommentForm, SubscriberForm
from ..models import Blog, Comment, User, Subscriber
from ..email import mail_message
from .. import db
import markdown2

@main.route('/')
def index():
    '''
    function that returns the index page
    '''
    blogs = Blog.query.all()
    return render_template('index.html', blogs = blogs)

@main.route('/new_blog', methods = ['GET','POST'])
@login_required
def new_blog():
   form  =BlogForm()

   if form.validate_on_submit():
       blog = form.blog.data

       new_blog = Blog(blog = blog, user_id = current_user.id)

       new_blog.save_blog()

       return redirect(url_for('main.index'))

   title = 'New Blog'
   return render_template('new_blog.html',title = title, blog_form = form)

@main.route('/comment/<id>')
def comment(id):
    '''
    function to return the comment
    '''
    comment = Comment.get_comment(id)
    print(comment)
    title = 'comments'
    return render_template('comment.html',title = title, comment = comment)

@main.route('/new_comment/<int:id>', methods = ['GET', 'POST'])
def new_comment(id):
    form = CommentForm()

    if form.validate_on_submit():
        writer = form.author.data
        com = form.comment.data

        new_comment = Comment(comment = com, blog_id = id, author= writer)
        new_comment.save_comment()

        return redirect(url_for('main.index'))

    title = 'New Comment'
    return render_template('new_comment.html', title = title, comment_form = form, pitch_id = id)

@main.route('/bloger/<uname>')
@login_required

def profile(uname):
    user = User.query.filter_by(username = uname).first()
    # abort(404)

    post = Blog.query.filter_by(user_id = current_user.id).all()
    print(post)


    title = uname

    return render_template('profile.html', user = user, blogs = post,title=title)

@main.route('/blog/<id>')
@login_required
def blog(id):

    post = Blog.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    print(post)

    title = 'Delete blog'

    return render_template('delete.html', title = title, blogs = post)

@main.route('/pro-comment/<id>')
@login_required
def viewcomment(id):
    '''
    function to return the comments
    '''
    comment = Comment.get_comment(id)
    print(comment)
    title = 'comments'
    return render_template('pro-comment.html',title = title, comment = comment)

@main.route('/del-comment/<id>')
@login_required
def delcomment(id):
    '''
    function to delete comments
    '''
    comment = Comment.query.filter_by(id = id).first()
    db.session.delete(comment)
    db.session.commit()
    print(comment)
    title = 'delete comments'
    return render_template('delete.html',title = title, comment = comment)

@main.route('/subscribe', methods=['GET','POST'])
def subscriber():

   subscriber_form=SubscriberForm()

   if subscriber_form.validate_on_submit():

       subscriber= Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)
       subscriber.save_subscriber()

       mail_message("Hello, New post on let us B-l-o-g.", "welcome_subscriber", subscriber.email,
                    subscriber=subscriber)

   subscriber = Blog.query.all()

   blog = Blog.query.all()

   return render_template('subscription.html', subscriber=subscriber, subscriber_form=subscriber_form, blog=blog)

@main.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    """
    Edit a blogpost in the database
    """
    new_blog=False

    blog = Blog.query.get(id)
    form = BlogForm()

    if form.validate_on_submit():

        blog.blog = form.blog.data

        db.session.commit()

        print('edited comment ')


        return redirect(url_for('main.index'))

    form.blog.data = blog.blog


    return render_template('new_blog.html',
                           action = 'Edit',
                           new_blog = new_blog,
                           blog_form = form,
                           legend='Update Post')
