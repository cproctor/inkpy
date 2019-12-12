from unittest import TestCase
from ink_runtime.object import RuntimeObject

# Testing Object on its own is difficult. The C# implementation is able to 
# import Container into Object, which we can't do because it would create a 
# circular import.

class TestObject(TestCase):
    def setUp(self):
        self.root = RuntimeObject()
        self.parent = RuntimeObject()
        self.child = RuntimeObject()
        self.parent.parent = self.root
        self.child.parent = self.parent

    def test_debug_line_number_of_path(self):
        # Depends on Container implementation
        pass

    def test_get_path(self):
        # Depends on Container implementation
        pass
        
    def test_root_content_container(self):
        self.assertIs(self.child.root_content_container(), self.root)

if __name__ == '__main__':
    unittest.main()

