from unittest import TestCase
from ink_runtime.path import Component, Path

class TestComponent(TestCase):
    def setUp(self):
        self.path = Path()
        self.index_c = Component(self.path, index=1)
        self.name_c = Component(self.path, name="name")

    def test_init_requires_index_or_name(self):
        with self.assertRaises(ValueError):
            Component(self.path)
    def test_init_requires_not_index_and_name(self):
        with self.assertRaises(ValueError):
            Component(self.path, index=1, name="haha")
    def test_is_index(self):
        self.assertTrue(self.index_c.is_index())
        self.assertFalse(self.name_c.is_index())
    def test_to_parent(self):
        p = self.index_c.to_parent()
        self.assertEqual(str(p), '^')
    def test_is_parent(self):
        p = self.index_c.to_parent()
        self.assertTrue(p.is_parent())
        self.assertFalse(self.index_c.is_parent())
    def test_eq(self):
        self.assertFalse(self.index_c == self.name_c)
        self.assertTrue(self.index_c == self.index_c)
        self.assertTrue(self.name_c == self.name_c)
        self.assertTrue(self.index_c == 1)
        self.assertFalse(self.index_c == 2)
        self.assertFalse(self.index_c == '1')
        self.assertTrue(self.name_c == 'name')
        self.assertFalse(self.name_c == 'othername')

if __name__ == '__main__':
    unittest.main()

