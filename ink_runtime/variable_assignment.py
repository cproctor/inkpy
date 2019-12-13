from typing import Optional
from ink_runtime.object import RuntimeObject

class VariableAssignemnt(RuntimeObject):

    def __init__(self, variable_name:sOptional[str]=None, is_new_declaration:bool=False):
        self.variable_name = variable_name
        self.is_new_declaration = is_new_declaration
        self.is_global = False

    def __str__(self):
        return "VarAssign to {}".format(self.variable_name)

