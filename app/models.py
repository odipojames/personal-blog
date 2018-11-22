from flask_login import UserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    blog = db.relationship('Blog', backref = 'username', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f' {self.username}'

class Blog(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blog(cls, user_id):
        blog = Blog.query.filter_by(id=user_id).all()
        return blog

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    author = db.Column(db.String(255))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls, id):
        comment = Comment.query.filter_by(blog_id=id).all()
        return comment

class Subscriber(UserMixin, db.Model):
   __tablename__="subscribers"

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255))
   email = db.Column(db.String(255),unique = True,index = True)


   def save_subscriber(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def get_subscribers(cls,id):
       return Subscriber.query.all()


   def __repr__(self):
       return f'User {self.email}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
