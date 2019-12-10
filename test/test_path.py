from unittest import TestCase
from ink_runtime.path import Component, Path

class TestPath(TestCase):
    def setUp(self):
        self.empty = Path()
        self.one_path = Path([Component(name='this')])
        self.two_path = Path([Component(name='this'), Component(name='that')])
        self.three_path = Path([Component(name='this'), Component(name='that'), 
                Component(name='other')])

    def test_head(self):
        self.assertIsNone(self.empty.head())
        self.assertEqual(self.one_path.head(), 'this')

    def test_tail(self):
        self.assertEqual(len(self.empty.tail()), 0)
        self.assertEqual(len(self.one_path.tail()), 0)
        self.assertEqual(len(self.two_path.tail()), 1)

    def test_last_component(self):
        self.assertIsNone(self.empty.last_component())
        self.assertEqual(self.one_path.last_component(), 'this')

    def test_contains_named_component(self):
        self.assertFalse(self.empty.contains_named_component())
        ixpath = Path([Component(index=1)])
        self.assertFalse(ixpath.contains_named_component())
        self.assertTrue(self.one_path.contains_named_component())

    def test_add(self):
        self.assertEqual(len(self.empty + self.two_path), 2)
        self.assertEqual(len(self.one_path + self.two_path), 3)

    def test_get_components_string(self):
        self.assertEqual(self.empty.get_components_string(), '.')
        self.assertEqual(self.two_path.get_components_string(), 
                'this.that')
        self.two_path.is_relative = True
        self.assertEqual(self.two_path.get_components_string(), 
                '.this.that')

    def test_set_components_string(self):
        relative = Path(components_string = '.this.that')
        self.assertEqual(str(relative), '.this.that')

    def test_eq(self):
        self.assertEqual(self.one_path, self.one_path + self.empty)
        self.assertNotEqual(self.one_path, self.two_path)
        

