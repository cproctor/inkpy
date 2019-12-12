from typing import Iterable, Mapping, Dict, Optional, Union
from enum import Enum, Flag
from ink_runtime.named_content import NamedContentMixin
from ink_runtime.object import RuntimeObject
from ink_runtime.path import Path, Component
from ink_runtime.story_exception import StoryException
import logging

log = logging.getLogger(__name__)

class CountFlags(Flag):
    VISITS = 1
    TURNS = 2
    COUNT_START_ONLY = 4

class Container(NamedContentMixin, RuntimeObject):

    def __init__(self, name:Optional[str]=None):
        super().__init__()
        self.name = name
        self.content = []
        self.named_content = {}
        self.flags = CountFlags(0)

    def get_content(self) -> Iterable['RuntimeObject']:
        return self.content

    def set_content(self, value:'RuntimeObject'):
        self.add_content(value)

    def get_named_only_content(self) -> Dict[str, 'RuntimeObject']:
        indexed_content_names = [c.name for c in self.content if c and c.has_valid_name()]
        return dict((k,v) for k,v in self.named_content.items() if k not in indexed_content_names)

    def set_named_only_content(self, named_only_content:Mapping[str, 'RuntimeObject']):
        for name in self.get_named_only_content().keys():
            del self.named_content[name]
        for obj in named_only_content.values():
            if obj:
                self.add_to_named_content_only(obj)

    def get_flags(self) -> CountFlags:
        if self.flags == CountFlags.COUNT_START_ONLY:
            return CountFlags(0)
        else:
            return self.flags

    def set_flags(self, value:CountFlags):
        self.flags = value

    def get_visits_should_be_counted(self) -> bool:
        return bool(self.flags & CountFlags.VISITS)

    def set_visits_should_be_counted(self, value):
        if value:
            self.flags |= CountFlags.VISITS
        else:
            self.flags &= ~CountFlags.VISITS

    def get_turn_index_should_be_counted(self) -> bool:
        return bool(self.flags & CountFlags.TURNS)

    def set_turn_index_should_be_counted(self, value):
        if value:
            self.flags |= CountFlags.TURNS
        else:
            self.flags &= ~CountFlags.TURNS

    def get_counting_at_start_only(self) -> bool:
        return bool(self.flags & CountFlags.COUNT_START_ONLY)

    def set_counting_at_start_only(self, value):
        if value:
            self.flags |= CountFlags.COUNT_START_ONLY
        else:
            self.flags &= ~CountFlags.COUNT_START_ONLY

    def has_valid_name(self) -> bool:
        return self.name is not None and len(self.name) > 0

    # TODO I don't understand this function. It's not an effective depth-first search
    # because when self.content[0] is empty it doesn't move on to self.content[1]
    # TODO memoized in the c# source
    def path_to_first_leaf_content(self) -> Path:
        path = Path()
        container = self
        while container is not None:
            if len(container.content) > 0:
                path.components.append(Component(0))
                container = container.content[0].as_container()
            # This check is not part of the c# source, but is needed to prevent an 
            # infinite loop
            else:
                raise ValueError("Unexpectedly found empty container")
        return self.path + path

    def add_content(self, content:Union[RuntimeObject, Iterable[RuntimeObject]]):
        if isinstance(content, RuntimeObject):
            content = [content]
        for c in content:
            self.content.append(c)
            if c.parent is not None:
                raise ValueError("Content is already in {}".format(c.parent))
            c.parent = self
            self.try_add_named_content(c)

    def insert_content(self, content:RuntimeObject, index:int):
        self.content.insert(index, content)
        if content.parent is not None:
            raise ValueError("Content is already in {}".format(content.parent))
        content.parent = self
        self.try_add_named_content(content)

    def try_add_named_content(self, content:RuntimeObject):
        if content.has_valid_name():
            self.add_to_named_content_only(content)

    def add_to_named_content_only(self, content:RuntimeObject):
        content.parent = self
        # This check not included in the source
        if not content.has_valid_name():
            raise ValueError("Cannot add named content without valid name: {}".format(content))
        self.named_content[content.name] = content
    
    def add_contents_of_container(self, other_container:'Container'):
        for c in other_container.content:
            self.content.append(c)
            c.parent = self
            self.try_add_named_content(c)

    def content_with_path_component(self, component:Component) -> Optional[RuntimeObject]:
        if component.is_index():
            try:
                return self.content[component.index]
            except IndexError:
                return None
        elif component.is_parent():
            return self.parent
        else:
            try:
                return self.named_content[component.name]
            except KeyError:
                raise StoryException("Content {} not found at path {}".format(component.name, self.path))

    # TODO This method is clumsy because I haven't decided how to handle casting between Object and Container
    # in the Python version
    def content_at_path(self, path:Path, partial_path_length:Optional[int]=None):
        if partial_path_length is None:
            partial_path_length = len(path)
        current_container = self
        current_obj = None
        for i in range(partial_path_length):
            comp = path.components[i]
            if current_container is None:
                raise StoryException("Path continued, but previous object wasn't a container: {}".format(currentObj))
            current_obj = current_container.content_with_path_component(comp)
            current_container = current_obj.as_container()
        return current_obj

    # In the C# idiom, Objects are frequently cast as Container, resulting in either a Container or null
    # if the object's class is not an ancestor of Container (eg Values). The most idiomatic way to translate
    # this to Python would be checking whether isinstance(obj, Container), but I can't do that in 
    # RunTime object because I would have cyclical dependencies. I could do something like 
    # obj.__class__.__name__ == 'Container', but it seems cleaner and closer to the source to have an 
    # `as_container` method in RuntimeObject which returns None, and overriding it here to return Self.
    def as_container(self):
        return self

    def build_string_of_hierarchy(self, indentation:int, pointed_object:RuntimeObject):
        s = ''
        spaces_per_indent = 4
        indent = lambda: ' ' * (indentation * spaces_per_indent)
        s += indent() + '['
        if self.has_valid_name():
            s += " ({})".format(self.name)
        if self is pointed_object:
            s += "  <---"
        s += '\n'
        indentation += 1
        for i, c in enumerate(self.content):
            if isinstance(c, Container):
                s += c.build_string_of_hierarchy(indentation, pointed_object)
            else:
                s += indent()
                if c.__class__.__name__ == 'StringValue':
                    s += '"' + str(c).replace('\n', '\\n') + '"'
                else:
                    s += str(c)
            if i < len(self.content) - 1:
                s += ','
            if isinstance(c, Container) and c is pointed_object:
                s += "  <---"
            s += '\n'
        only_named = dict((k,v) for k,v in self.named_content.items() if v not in self.content)
        if len(only_named) > 0:
            s += indent() + "-- named: --"
            for k, v in only_named.items():
                if not isinstance(v, Container):
                    log.debug("Can only print out named Containers")
                s += v.build_string_of_hierarchy(indentation, pointed_object)
                s += '\n'
        indentation -= 1
        s += indent() + ']'
        return s
                
