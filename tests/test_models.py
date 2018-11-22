import  unittest
from app.models import User,Comment,Blog,Subscriber

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(password='blog')

    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('blog'))

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.new_comment = Comment(id = 1, comment = 'ok', author = 'oj', blog_id = 1)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))

    def test_variables(self):
        self.assertEquals(self.new_comment.id,1)
        self.assertEquals(self.new_comment.comment, 'ok')
        self.assertEquals(self.new_comment.author, 'oj')
        self.assertEquals(self.new_comment.blog_id, 1)

    def test_get_comment(self):
        # self.new_comment.save_comment()
        self.get_comments = Comment.get_comment(1)
        self.assertEquals(self.get_comments, [] )

class BlogModelTest(unittest.TestCase):

    def setUp(self):
        self.new_blog = Blog(id = 1, blog = 'ok',user_id = 1)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))

    def test_variables(self):
        self.assertEquals(self.new_blog.id,1)
        self.assertEquals(self.new_blog.blog, 'ok')
        self.assertEquals(self.new_blog.user_id, 1)

    def test_get_blog(self):
        self.get_blog = Blog.get_blog(1)
        self.assertEquals(self.get_blog, [])

class SubscriberModelTest(unittest.TestCase):

    def setUp(self):
        self.new_subscriber = Subscriber(id = 1 , name = 'ok', email = 'he')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_subscriber,Subscriber))

    def test_variables(self):
        self.assertEquals(self.new_subscriber.id, 1)
        self.assertEquals(self.new_subscriber.name, 'ok')
        self.assertEquals(self.new_subscriber.email, 'he')
