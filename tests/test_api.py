import unittest
from werkzeug.exceptions import NotFound
from app import create_app, db
from app.models import Component
from .test_client import TestClient


class TestAPI(unittest.TestCase):
    default_username = 'dave'
    default_password = 'cat'

    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = TestClient(self.app, 'auth-token', '')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_components(self):
        # get list of components
        rv, json = self.client.get('/api/components/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['components'] == [])

        # add a component
        rv, json = self.client.post('/api/components/',
                                    data={'ident': 'M1'})
        self.assertTrue(rv.status_code == 201)
        location = rv.headers['Location']
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'M1')
        rv, json = self.client.get('/api/components/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['components'] == [location])

        # edit the component
        rv, json = self.client.put(location, data={'ident': 'M2'})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'M2')
