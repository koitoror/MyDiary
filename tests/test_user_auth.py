import unittest
from app.models import User
from app.application import Application


class TestUserAuthentication(unittest.TestCase):
    """
    Class to test the user authentication, both the registration
    and login.
    """

    def setUp(self):
        self.user = User('koitoror', '123456', 'kamarster')
        self.app = Application()

    def test_user_is_added_to_dictionary_when_created(self):
        self.assertTrue(self.app.register_user(User('kamar1', '123456', 'kamarster')))

    def test_user_already_exists_in_user_dictionary(self):
        self.app.users = {'koitoror': self.user}
        self.assertFalse(self.app.register_user(self.user))

    def test_user_sigining_in_is_already_registered(self):
        self.app.users = {'koitoror': self.user}
        self.assertTrue(self.app.does_user_exist('koitoror'))

    def test_user_trying_to_login_has_entered_a_correct_password(self):
        self.app.users = {'koitoror': self.user}
        self.assertTrue(self.app.login_user('koitoror', '123456'))

    def test_user_trying_to_login_has_entered_a_wrong_password(self):
        self.app.users = {'koitoror': self.user}
        self.assertFalse(self.app.login_user('koitoror', 'sdfgdsfj'))


if __name__ == '__main__':
    unittest.main()
