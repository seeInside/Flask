import unittest
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        
        with self.assertRaises(TypeError):
            u.password

    def test_password_verify(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('asd'))

    def test_password_salts_are_random(self):
        u = User(password = 'cat')
        u1 = User()
        u1.password = 'cat'
        self.assertFalse(u.password_hash == u1.password_hash)
    def test_roles_and_permission(self):
        Role.insert_roles()
        u = User(email = '444324681@qq.com', password = '3344521')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

        
