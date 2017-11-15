from unittest import TestCase

from app.core.analysis import Component, SubComponent


class SubComponent(TestCase):
    pass


class ComponentTestCase(TestCase):

    def setUp(self):
        self.component = Component('Manifold')

    def add_subcomponent(self, description='Actuated Process Valve', ident='V1'):
        self.component.add_subcomponent(description, ident)

    def add_consequence(self, name='major', cost=1000):
        self.component.add_consequence(name, cost)


class TestComponent(ComponentTestCase):

    def test_add_subcomponent(self):
        self.add_subcomponent()
        self.assertTrue(
            any(sc.description == 'Actuated Process Valve' and sc.ident == 'V1' for sc in self.component.subcomponents))

    def test_add_consequence(self):
        self.add_consequence()
        self.assertEqual(self.component.consequences['major'], 1000)
        # self.assertIn()

    def test_risk(self):
        self.add_subcomponent()
        self.add_subcomponent()
        self.add_consequence()


class SubComponent(ComponentTestCase):

    def test_risks(self):
        self.add_subcomponent()
        self.add_consequence()
