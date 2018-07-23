import unittest
from app.models import User, Diary


class TestUserDiary(unittest.TestCase):
    def setUp(self):
        self.user = User('koitoror', '12345')

    def test_user_can_create_diary(self):
        diary = Diary("Lorem ipsum dolor", "Hey")
        self.assertTrue(self.user.create_diary(diary))

    def test_user_diary_already_exists(self):
        diary = Diary("Lorem ipsum dolor", "Hey")
        self.user.entries = {"Lorem ipsum dolor": diary}
        self.assertFalse(self.user.create_diary(diary))

    def test_a_diary_is_returned_when_an_id_is_specified(self):
        diary = Diary("Lorem ipsum dolor", "Hey")
        self.user.entries = {"Lorem ipsum dolor": diary}
        self.assertEqual(self.user.get_diary("Lorem ipsum dolor"), diary)

    def test_none_is_returned_for_a_diary_that_does_not_exist(self):
        self.assertIsNone(self.user.get_diary("ABGDTAD"))

    def test_a_diary_is_updated(self):
        diary = Diary("Lorem ipsum dolor", "Hey")
        self.user.entries = {"Lorem ipsum dolor": diary}
        self.user.update_diary("Lorem ipsum dolor", 'Sleeping')
        self.assertEqual(self.user.get_diary("Lorem ipsum dolor").name, "Sleeping")

    def test_the_diary_to_be_updated_does_not_exist(self):
        self.assertFalse(self.user.update_diary("BDBHGF", "Playing"))

    def test_a_diary_is_successfully_deleted(self):
        diary = Diary("Lorem ipsum dolor", "Hey")
        self.user.entries = {"Lorem ipsum dolor": diary}
        self.user.delete_diary("Lorem ipsum dolor")
        self.assertEqual(self.user.entries, {})

    def test_false_is_returned_when_deleting_un_existing_diary(self):
        self.assertFalse(self.user.delete_diary("Lorem ipsum dolor"))

if __name__ == '__main__':
    unittest.main()
