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

    def test_areas_and_components(self):
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

        # create an area
        rv, json = self.client.post(areas_url,
                                    data={'name': 'DC1',
                                          'remaining_life': 7,
                                          'equity_share': 0.72})
        self.assertTrue(rv.status_code == 201)
        area = rv.headers['Location']
        rv, json = self.client.get(area)
        components_url = json['components_url']
        rv, json = self.client.get(components_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['components'] == [])
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

        # add two components to area
        rv, json = self.client.post(components_url, data={'ident': 'M1'})
        self.assertTrue(rv.status_code == 201)
        component1 = rv.headers['Location']
        rv, json = self.client.post(components_url, data={'ident': 'SUT1'})
        self.assertTrue(rv.status_code == 201)
        component2 = rv.headers['Location']
        rv, json = self.client.get(components_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['components']) == 2)
        self.assertTrue(component1 in json['components'])
        self.assertTrue(component2 in json['components'])
        rv, json = self.client.get(component1)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'M1')
        self.assertTrue(json['area_url'] == area)
        rv, json = self.client.get(component2)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'SUT1')
        self.assertTrue(json['area_url'] == area)

        # edit the second component
        rv, json = self.client.put(component2, data={'ident': 'SUT2'})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(component2)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'SUT2')
        self.assertTrue(json['area_url'] == area)

        # delete first component
        rv, json = self.client.delete(component1)
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(components_url)
        self.assertFalse(component1 in json['components'])
        self.assertTrue(component2 in json['components'])

        # delete area
        rv, json = self.client.delete(area)
        self.assertTrue(rv.status_code == 200)
        with self.assertRaises(NotFound):
            rv, json = self.client.get(component2)
        rv, json = self.client.get('/api/areas/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['areas']) == 0)

    def test_subcomponents(self):
        # define a facility
        rv, json = self.client.post('/api/facilities/',
                                    data={'name': 'Foinaven'})
        facility = rv.headers['Location']
        rv, json = self.client.get(facility)
        areas_url = json['areas_url']
        rv, json = self.client.get(areas_url)

        # create an area
        rv, json = self.client.post(areas_url,
                                    data={'name': 'DC1',
                                          'remaining_life': 7,
                                          'equity_share': 0.72})
        area = rv.headers['Location']
        rv, json = self.client.get(area)
        components_url = json['components_url']

        # create a component
        rv, json = self.client.post(components_url, data={'ident': 'M1'})
        component = rv.headers['Location']
        rv, json = self.client.get(component)
        subcomponents_url = json['subcomponents_url']

        # add two subcomponents to component
        rv, json = self.client.post(subcomponents_url, data={'ident': 'D1',
                                                             'category': 'cat1'})
        self.assertTrue(rv.status_code == 201)
        subcomponent1 = rv.headers['Location']
        rv, json = self.client.post(subcomponents_url, data={'ident': 'D2',
                                                             'category': 'cat2'})
        self.assertTrue(rv.status_code == 201)
        subcomponent2 = rv.headers['Location']
        rv, json = self.client.get(subcomponents_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['subcomponents']) == 2)
        self.assertTrue(subcomponent1 in json['subcomponents'])
        self.assertTrue(subcomponent2 in json['subcomponents'])
        rv, json = self.client.get(subcomponent1)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'D1')
        self.assertTrue(json['category'] == 'cat1')
        self.assertTrue(json['component_url'] == component)
        rv, json = self.client.get(subcomponent2)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'D2')
        self.assertTrue(json['category'] == 'cat2')
        self.assertTrue(json['component_url'] == component)

        # edit the second subcomponent
        rv, json = self.client.put(subcomponent2, data={'ident': 'C1',
                                                        'category': 'cat3'})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(subcomponent2)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['ident'] == 'C1')
        self.assertTrue(json['category'] == 'cat3')
        self.assertTrue(json['component_url'] == component)

        # delete first subcomponent
        rv, json = self.client.delete(subcomponent1)
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(subcomponents_url)
        self.assertFalse(subcomponent1 in json['subcomponents'])
        self.assertTrue(subcomponent2 in json['subcomponents'])
