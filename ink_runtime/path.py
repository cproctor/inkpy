# https://github.com/inkle/ink/blob/master/ink-engine-runtime/Path.cs

from typing import Optional, Iterable, Union

class Component:

    # Returns a component indicating the component's parent
    @classmethod
    def to_parent(cls) -> 'Component':
        return Component(name=Path.parent_id)

    def __init__(self, path:Optional['Path']=None, index:Optional[int]=None, name:Optional[str]=None):
        if index is None and name is None:
            raise ValueError("Component must be initialized with index or name")
        if index is not None and name is not None:
            raise ValueError("Component must be initialized with index or name, but not both")
        self.path = path
        self.index = index
        self.name = name

    def is_index(self) -> bool:
        return self.index is not None

    def is_parent(self) -> bool:
        return self.name == Path.parent_id

    def __str__(self) -> str:
        return str(self.index if self.is_index() else self.name)

    def __eq__(self, other) -> bool:
        if isinstance(other, Component):
            sid = self.index if self.is_index() else self.name
            oid = other.index if other.is_index() else other.name
            return sid == oid
        else:
            return (self.index if self.is_index() else self.name) == other

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self):
        return hash(self.index if self.is_index() else self.name)

class Path:
    parent_id = '^'

    # Returns a Path to oneself (eg '.' in shell)
    @classmethod
    def self(cls):
        return Path(relative=True)

    # Not in 0.3.3, but in Master.
    def get_component(self, index:int) -> Component:
        return self.components[index]
     
    def head(self) -> Optional[Component]:
        return self.components[0] if len(self.components) else None

    def tail(self) -> 'Path':
        if len(self) >= 2:
            return Path(components=self.components[1:])
        else:
            return Path.self()

    def __len__(self) -> int:
        return len(self.components)

    def last_component(self) -> Optional[Component]:
        return self.components[-1] if len(self.components) else None

    def contains_named_component(self) -> bool:
        return any(not c.is_index() for c in self.components)

    def __init__(self, 
        components:Optional[Iterable[Component]]=None, 
        head:Optional[Component]=None,
        tail:Optional['Path']=None,
        components_string:Optional[str]=None,
        relative=None
    ):
        if components is not None:
            self.components = components
            for c in self.components:
                c.path = self
            self.is_relative = relative
        elif head is not None and tail is not None:
            self.components = [head] + tail.components
            self.is_relative = relative
        elif components_string is not None:
            self.set_components_string(components_string)
        else:
            self.components = []
            self.is_relative = True

    # Inplements PathByAppendingPath and PathByAppendingComponent
    def __add__(self, other:Union[Component, 'Path']) -> 'Path':
        if isinstance(other, Component):
            return Path(self.components + [Component])
        else:
            return Path(self.components + other.components)

    def get_components_string(self) -> str:
        return ('.' if self.is_relative else '') + ".".join(str(c) for c in self.components)
    
    def set_components_string(self, cs:Optional[str]) -> None:
        self.components = []
        if cs:
            segments = cs.split('.')
            if segments[0] == '':
                self.is_relative = True
                segments = segments[1:]
            for seg in segments:
                if seg.isdigit():
                    self.components.append(Component(self, index=int(seg)))
                else:
                    self.components.append(Component(self, name=seg))
                    
    def __str__(self) -> str:
        return self.get_components_string()

    def __eq__(self, other:'Path'):
        if self.is_relative != other.is_relative:
            return False
        if len(self.components) != len(other.components):
            return False
        return all(sc == oc for sc, oc in zip(self.components, other.components))

    def __hash__(self):
        return hash(tuple(hash(c) for c in self.components))

    




