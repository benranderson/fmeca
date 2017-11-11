import unittest
from werkzeug.exceptions import NotFound
from app import create_app, db
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

    def test_facilities(self):
        # get list of facilities
        rv, json = self.client.get('/api/facilities/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['facilities'] == [])

        # add a facility
        rv, json = self.client.post('/api/facilities/',
                                    data={'name': 'Foinaven'})
        self.assertTrue(rv.status_code == 201)
        location = rv.headers['Location']
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'Foinaven')
        rv, json = self.client.get('/api/facilities/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['facilities'] == [location])

        # edit the facility
        rv, json = self.client.put(location, data={'name': 'Andrew'})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'Andrew')

        # delete the facility
        rv, json = self.client.delete(location)
        self.assertTrue(rv.status_code == 200)
        with self.assertRaises(NotFound):
            rv, json = self.client.get(location)
        rv, json = self.client.get('/api/facilities/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['facilities']) == 0)

    def test_areas(self):
        # define a facility
        rv, json = self.client.post('/api/facilities/',
                                    data={'name': 'Foinaven'})
        self.assertTrue(rv.status_code == 201)
        facility = rv.headers['Location']
        rv, json = self.client.get(facility)
        areas_url = json['areas_url']
        rv, json = self.client.get(areas_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['areas'] == [])

        # # define two areas
        # rv, json = self.client.post('/api/areas/',
        #                             data={'name': 'DC1',
        #                                   'remaining_life': 7,
        #                                   'equity_share': 0.72})
        # self.assertTrue(rv.status_code == 201)
        # area1 = rv.headers['Location']
        # rv, json = self.client.post('/api/areas/',
        #                             data={'name': 'DC2A',
        #                                   'remaining_life': 7,
        #                                   'equity_share': 0.42})
        # self.assertTrue(rv.status_code == 201)
        # area2 = rv.headers['Location']

        # create an area
        rv, json = self.client.post(areas_url,
                                    data={'name': 'DC1',
                                          'remaining_life': 7,
                                          'equity_share': 0.72})
        self.assertTrue(rv.status_code == 201)
        area = rv.headers['Location']
        rv, json = self.client.get(area)
        # items_url = json['items_url']
        # rv, json = self.client.get(items_url)
        # self.assertTrue(rv.status_code == 200)
        # self.assertTrue(json['items'] == [])
        rv, json = self.client.get('/api/areas/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['areas']) == 1)
        self.assertTrue(area in json['areas'])

        # edit the area
        rv, json = self.client.put(area,
                                   data={'name': 'DC2A',
                                         'remaining_life': 5,
                                         'equity_share': 0.42})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(area)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'DC2A')
        self.assertTrue(json['remaining_life'] == 5)
        self.assertTrue(json['equity_share'] == 0.42)

        # delete area
        rv, json = self.client.delete(area)
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get('/api/areas/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['areas']) == 0)

        # # add two items to order
        # rv, json = self.client.post(items_url, data={'product_url': prod1,
        #                                              'quantity': 2})
        # self.assertTrue(rv.status_code == 201)
        # item1 = rv.headers['Location']
        # rv, json = self.client.post(items_url, data={'product_url': prod2,
        #                                              'quantity': 1})
        # self.assertTrue(rv.status_code == 201)
        # item2 = rv.headers['Location']
        # rv, json = self.client.get(items_url)
        # self.assertTrue(rv.status_code == 200)
        # self.assertTrue(len(json['items']) == 2)
        # self.assertTrue(item1 in json['items'])
        # self.assertTrue(item2 in json['items'])
        # rv, json = self.client.get(item1)
        # self.assertTrue(rv.status_code == 200)
        # self.assertTrue(json['product_url'] == prod1)
        # self.assertTrue(json['quantity'] == 2)
        # self.assertTrue(json['order_url'] == order)
        # rv, json = self.client.get(item2)
        # self.assertTrue(rv.status_code == 200)
        # self.assertTrue(json['product_url'] == prod2)
        # self.assertTrue(json['quantity'] == 1)
        # self.assertTrue(json['order_url'] == order)

        # # edit the second item
        # rv, json = self.client.put(item2, data={'product_url': prod2,
        #                                         'quantity': 3})
        # self.assertTrue(rv.status_code == 200)
        # rv, json = self.client.get(item2)
        # self.assertTrue(rv.status_code == 200)
        # self.assertTrue(json['product_url'] == prod2)
        # self.assertTrue(json['quantity'] == 3)
        # self.assertTrue(json['order_url'] == order)

        # # delete first item
        # rv, json = self.client.delete(item1)
        # self.assertTrue(rv.status_code == 200)
        # rv, json = self.client.get(items_url)
        # self.assertFalse(item1 in json['items'])
        # self.assertTrue(item2 in json['items'])

        # # delete order
        # rv, json = self.client.delete(order)
        # self.assertTrue(rv.status_code == 200)
        # with self.assertRaises(NotFound):
        #     rv, json = self.client.get(item2)
        # rv, json = self.client.get('/api/v1/orders/')
        # self.assertTrue(rv.status_code == 200)
        # self.assertTrue(len(json['orders']) == 0)

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

        # delete the component
        rv, json = self.client.delete(location)
        self.assertTrue(rv.status_code == 200)
        with self.assertRaises(NotFound):
            rv, json = self.client.get(location)
        rv, json = self.client.get('/api/components/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['components']) == 0)
