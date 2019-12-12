# TODO Do I need to cast stuff to Containers?
from typing import Optional
from ink_runtime.debug_metadata import DebugMetadata
from ink_runtime.path import Path
from ink_runtime.search_result import SearchResult
import logging

log = logging.getLogger(__name__)

class RuntimeObject:
    parent = None
    debug_metadata = None
    
    def __init__(self, path:Path=None):
        self.path = path

    def debug_line_number_of_path(path:Optional[Path]) -> Optional[int]:
        root = self.root_content_container()
        if root and path:
            target_content = root.content_at_path(path)
            if target_content:
                dm = target_content.debug_metadata
                if dm:
                    return dm.start_line_number

    def get_path(self):
        if self.parent is None:
            return Path()
        else:
            comps = []
            child = self
            container = child.parent.as_container()
            while container:
                if child.has_valid_name():
                    comps.append(Component(name=child.name))
                else:
                    comps.append(Component(index=container.content.index_of(child)))
                child = container
                container = container.parent.as_container()
            return Path(comps)

    def content_at_path(self, path):
        raise NotImplementedError()

    def as_container(self):
        log.debug("Casting RuntimeObject to Container; always fails with None")
        return None

    def resolve_path(self, path:Path) -> SearchResult:
        if path.is_relative:
            nearest_container = self.as_container()
            if nearest_container is None:
                if self.parent is None:
                    log.debug("Can't resolve relative path because we don't have a parent")
                nearest_container = self.parent.as_container()
                if nearest_container is None:
                    log.debug("Expected parent to be a container")
                if not path.get_component(0).is_parent:
                    log.debug("Expected component 0 to be a parent")
                path = path.tail()
            return nearest_container.content_at_path(path)
        else:
            return self.root_content_container().content_at_path(path)

    def convert_to_relative_path(self, global_path:Path) -> Path:
        own_path = self.path
        min_path_length = min(len(global_path), len(own_path))
        last_shared_path_comp_index = None
        for i in range(min_path_length):
            own_comp = own_path.get_component(i)
            other_comp = global_path.get_component(i)
            if own_comp == other_comp:
                last_shared_path_comp_index = i
            else:
                break
        if last_shared_path_comp_index is None:
            return global_path
        num_upwards_moves = len(own_path) - 1 - last_shared_path_comp_index
        new_path_comps = []
        for up in range(num_upwards_moves):
            new_path_comps.append(Component.to_parent())
        for down in range(last_shared_path_comp_index + 1, len(global_path)):
            new_path_comps.append(global_path.get_component(down))
        return Path(components=new_path_comps, relative=True)

    def compact_path_string(other_path:Path) -> str:
        if other_path.is_relative:
            relative_path_str = other_path.get_components_string()
            global_path_str = (self.path + other_path).get_components_string()
        else:
            relative_path_str = self.convert_to_relative_path(other_path).get_components_string()
            global_path_str = other_path.get_components_string()
        if len(relative_path_string) < len(global_path_string):
            return relative_path_string
        else:
            return global_path_str

    # TODO Decide whether to specify Container output type
    def root_content_container(self):
        ancestor = self
        while ancestor.parent is not None:
            ancestor = ancestor.parent
        return ancestor
        
    # Don't fully understand. See source line 196
    def set_child(self, obj:'Object', value:'Object'):
        if obj:
            obj.parent = None
        obj = value
        if obj:
            obj.parent = self

    # Note: Skipped type casting code from 209. I don't think it's necessary, but not sure.









            
        
