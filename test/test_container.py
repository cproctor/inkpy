from unittest import TestCase
from ink_runtime.container import Container, CountFlags
from ink_runtime.object import RuntimeObject
from ink_runtime.path import Component

class TestContainer(TestCase):
    def setUp(self):
        self.named = Container(name="name")
        self.anon = Container()
        self.content = Container(name="content")
        self.other_content = Container(name="other_content")
        self.parent = Container()
        self.parent.set_content(self.named)
        self.parent.set_content(self.anon)
    
    def test_get_content(self):
        self.assertEqual(len(self.named.content), 0)
        self.named.set_content(self.content)
        self.assertIs(self.named.get_content()[0], self.content)

    def test_set_content_adds_to_content(self):
        self.assertEqual(len(self.named.content), 0)
        self.named.set_content(self.content)
        self.assertEqual(len(self.named.content), 1)

    def test_set_content_tries_to_add_to_named_content(self):
        self.assertEqual(self.parent.named_content["name"], self.named)
        self.assertEqual(len(self.parent.named_content), 1)

    def test_get_named_only_content(self):
        self.parent.named_content['content'] = self.content
        c = self.parent.get_named_only_content()
        self.assertIs(c['content'], self.content)
        self.assertEqual(len(c), 1)

    def test_set_named_only_content_deletes_existing_keys(self):
        self.parent.named_content['content'] = self.content
        self.assertEqual(len(self.parent.named_content), 2)
        self.parent.set_named_only_content({})
        self.assertEqual(len(self.parent.content), 2)
        self.assertEqual(len(self.parent.named_content), 1)

    def test_set_named_only_content_adds_only_to_named_content(self):
        self.parent.set_named_only_content({'content': self.content})
        self.assertEqual(len(self.parent.named_content), 2)
        self.assertEqual(len(self.parent.content), 2)

    def test_get_and_set_visits_should_be_counted(self):
        self.assertFalse(self.parent.get_visits_should_be_counted())
        self.parent.set_visits_should_be_counted(False)
        self.assertFalse(self.parent.get_visits_should_be_counted())
        self.parent.set_visits_should_be_counted(True)
        self.assertTrue(self.parent.get_visits_should_be_counted())

    def test_set_multiple_turn_count_flags(self):
        self.parent.set_flags(CountFlags.TURNS | CountFlags.COUNT_START_ONLY)
        self.assertTrue(self.parent.get_turn_index_should_be_counted())
        self.assertFalse(self.parent.get_visits_should_be_counted())
        self.assertTrue(self.parent.get_counting_at_start_only())

    def test_path_to_first_leaf_content(self):
        return # TODO Change RuntimeObject to something which implements the NamedContentMixin
        stuff = RuntimeObject()
        self.named.add_content(RuntimeObject())
        print(self.parent.path_to_first_leaf_content())
        
    def test_add_content_with_single_value(self):
        self.assertEqual(len(self.named.content), 0)
        self.assertEqual(len(self.named.named_content), 0)
        self.named.add_content(self.content)
        self.assertEqual(len(self.named.content), 1)
        self.assertEqual(len(self.named.named_content), 1)

    def test_add_content_with_list(self):
        self.assertEqual(len(self.named.content), 0)
        self.assertEqual(len(self.named.named_content), 0)
        self.named.add_content([self.content, self.other_content])
        self.assertEqual(len(self.named.content), 2)
        self.assertEqual(len(self.named.named_content), 2)

    def test_insert_content(self):
        self.parent.insert_content(self.content, 1)
        self.assertEqual(len(self.parent.content), 3)
        self.assertIs(self.parent.content[1], self.content)

    def test_add_to_named_content_only(self):
        pass

    def test_add_contents_of_container(self):
        pass

    def test_content_with_path_component_for_index(self):
        self.assertIs(self.parent.content_with_path_component(Component(index=0)), self.named)
        self.assertIs(self.parent.content_with_path_component(Component(index=1)), self.anon)

    def test_content_with_path_component_for_name(self):
        self.assertIs(self.parent.content_with_path_component(Component(name="name")), self.named)

    def test_content_with_path_component_for_parent(self):
        self.assertIs(self.named.content_with_path_component(Component(name="^")), self.parent)

    def test_content_at_path(self):
        pass

    def test_content_at_path_with_partial_path_length(self):
        pass

    def test_build_string_of_hierarchy(self):
        pass
    

if __name__ == '__main__':
    unittest.main()
