from flask_testing import TestCase
from app.apis.models.entries import Entry
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    @classmethod
    def create_app(cls):
        app.config.from_object('app.apis.config.TestingConfig')
        return app

    def setUp(self):
        self.entry = Entry()
        self.data = self.entry.create_entry({"title":"test1", "contents":"contents1"})
        self.no_title = self.entry.create_entry({"contents": "no title"})
        self.no_contents = self.entry.create_entry({"title": "no contents"})

    def tearDown(self):
        self.entry.no_of_entries.clear()
