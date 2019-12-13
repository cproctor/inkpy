from ink_runtime.path import Path
from ink_runtime.object import RuntimeObject

class VariableReference(RuntimeObject):
    
    def get_container_for_count(self):
        return self.resolve_path(self.path_for_count).to_container()

    def get_path_string_for_count(self):
        if self.path_for_count is None:
            return None
        else:
            return self.compact_path_string(self.path_for_count) 

    def set_path_string_for_count(self, value):
        if value is None:
            self.path_for_count = None
        else:
            self.path_for_count = Path(value)

    def __init__(self, name):
        self.name = name
        self.path_for_count = None

    def __str__(self):
        if self.name is None:   
            return "read_count({})".format(self.get_path_string_for_count()) 
        else:
            return "var({})".format(self.name)
        

