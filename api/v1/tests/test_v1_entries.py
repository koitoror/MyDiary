import unittest
import json
from versions import app
from versions.v1.models import User, db, entries


class TestEntriesV1(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.Testing')
        self.app = app.test_client()
        self.new_entries_info = {
            "date": "12-07-2018 09:40:38", 
            "title": "Hey", 
            "text": "", 
            "entryId": ["one", "purple", "two", "three", "four"]
        }
        self.modify_entries_info = {
            "date": "12-07-2018 09:40:38", 
            "title": "Hey", 
            "text": "", 
            "entryId": ["one", "purple", "two", "three", "four"]
        }
        self.new_user_info = {
            "username": "Admin",
            "fullname": "daniel kamar",
            "email": "kamarster@gmail.com",
            "password": "12345"
        }
        self.user_login_info = {
            "username": "Admin",
            "password": "12345"
        }

    def test_read_all_entries(self):
        """Test if can access endpoint for all entries
        """
        self.register_entries()
        response = self.app.get('/api/v1/entries/')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.get_data(as_text=True))['entries']
        self.assertEqual(output[0]['name'], self.new_entries_info['name'])

    def test_read_if_no_entries(self):
        """Test what happens when no entries
        """
        response = self.app.get('/api/v1/entries/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('No entries, create one first', str(response.data))

    def test_create_entries(self):
        """Test if can register new entries
        """
        response = self.register_entries()
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'successfully created entries')
        exists = db.session.query(
            db.exists().where(entries.name == output['entries']['name'])
        ).scalar()
        self.assertTrue(exists)

    def test_create_entries_if_name_taken(self):
        """Test create entries if name is taken
        """
        self.register_entries()
        response = self.register_entries()
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(
            output,
            'entries name {} already taken'.format(
                self.new_entries_info['name']))

    def test_can_read_one_entry(self):
        """Test route for single entry
        """
        new_entries = self.register_entry()
        entries_id = json.loads(
            new_entries.get_data(as_text=True))['entries']['id']

        response = self.app.get('/api/v1/entries/{}'.format(entries_id))
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.get_data(as_text=True))['entries']
        self.assertEqual(output['id'], entries_id)

    def test_read_no_entries(self):
        """Test 404 not found on entries not existing
        """
        response = self.app.get('/api/v1/entries/6000')
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'entries Not Found')

    def test_modify_entries(self):
        """Test if user can modify entries
        """
        new_entries = self.register_entries()
        entries_id = json.loads(
            new_entries.get_data(as_text=True))['entries']['id']

        response = self.app.put(
            '/api/v1/entries/{}'.format(entries_id),
            data=json.dumps(self.modify_entries_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertIn('successfully modified', str(response.data))
        _entries = json.loads(response.get_data(as_text=True))
        exists = db.session.query(
            db.exists().where(entries.name == _entries['entries']['name']))
        self.assertTrue(exists)

    def test_unsuccesful_modify(self):
        """Test modify if entries doesn't exist"""
        self.register_user()
        response = self.app.put(
            '/api/v1/entries/6000',
            data=json.dumps(self.modify_entries_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertIn('entries Not Found', str(response.data))
        self.assertEqual(response.status_code, 404)

    def test_delete_entries_not_owner(self):
        """Test delete not your entries
        """
        self.new_user_info = {
            "username": "Admin",
            "fullname": "daniel kamar",
            "email": "kamarster@gmail.com",
            "password": "12345"
        }
        self.user_login_info = {
            "username": "Admin",
            "password": "12345"
        }
        self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        response_login = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(new_user_login),
            content_type='application/json'
        )
        token = json.loads(response_login.get_data(as_text=True))['token']
        new_entries = self.register_entries()
        entries_id = json.loads(
            new_entries.get_data(as_text=True))['entries']['id']

        response = self.app.delete(
            '/api/v1/entries/{}'.format(entries_id),
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 401)

        self.assertIn('Not Allowed, you are not owner', str(response.data))

    def test_delete_entries(self):
        """Test if actually deleted entries
        """
        new_entries = self.register_entries()
        entries_id = json.loads(
            new_entries.get_data(as_text=True))['entries']['id']

        response = self.app.delete(
            '/api/v1/entries/{}'.format(entries_id),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('entries Deleted', str(response.data))

    def test_delete_empty_entries(self):
        """Test delete already deleted entries
        """
        self.register_user()
        response = self.app.delete(
            '/api/v1/entries/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('entries Not Found', str(response.data))

if __name__ == '__main__':
    unittest.main()
