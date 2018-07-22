import unittest
from app.models import diary
from app.models import diaryItem


class TestdiaryItems(unittest.TestCase):
    def setUp(self):
        self.diary = diary("Lorem ipsum dolor", "Hey")

    def test_user_can_create_diary(self):
        item = diaryItem('XZBNVLK', 'Kampala', 'Find Baganda', '2018-07-27')
        self.assertTrue(self.diary.create_item(item))

    def test_item_already_exists_in_the_diary(self):
        item = diaryItem('XZBNVLK', 'Kampala', 'Find Baganda', '2018-07-27')
        self.diary.items = {'XZBNVLK': item}
        self.assertFalse(self.diary.create_item(item))

    def test_an_item_in_the_diary_is_returned_when_an_id_is_specified(self):
        item = diaryItem('XZBNVLK', 'Kampala', 'Find Baganda', '2018-07-27')
        self.diary.items = {'XZBNVLK': item}
        self.assertEqual(self.diary.get_item(item.id), item)

    def test_none_is_returned_when_an_item_is_not_found_by_its_id(self):
        self.assertIsNone(self.diary.get_item("VBDHJFS"))

    def test_that_an_item_in_a_diary_is_updated(self):
        item = diaryItem('XZBNVLK', 'Kampala', 'Find Baganda', '2018-07-27')
        self.diary.items = {'XZBNVLK': item}
        self.diary.update_item('XZBNVLK', 'Nairobi', "Find Baganda", '2018-07-27')
        self.assertEqual(self.diary.get_item('XZBNVLK').name, 'Nairobi')

    def test_item_to_be_updated_is_missing(self):
        self.assertFalse(self.diary.update_item('AGHGJC', 'Kampala', 'Find Baganda', '2018-07-27'))

    def test_item_is_successfully_deleted(self):
        item = diaryItem('XZBNVLK', 'Kampala', 'Find Baganda', '2018-07-27')
        self.diary.items = {'XZBNVLK': item}
        self.diary.delete_item('XZBNVLK')
        self.assertEqual(self.diary.items, {})

    def test_an_item_that_does_not_exist_cannot_be_deleted(self):
        self.assertFalse(self.diary.delete_item("HJJJFG"))


if __name__ == '__main':
    unittest.main()
