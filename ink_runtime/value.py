from enum import Enum, auto
from ink_runtime.object import RuntimeObject
from ink_runtime.path import Path

# Should we really be implementing a dynamic type system on top of the 
# one we already have? There are cleaner ways to do this in Python, 
# but this will only ever be used internally to this package, so it's
# probably better on the whole to hew to a closer translation.

class ValueType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    DIVERT_TARGET = auto()
    VARIABLE_POINTER = auto()

class Value(RuntimeObject):

    value_type = None

    def default_value(self):
        return None

    def get_value_type(self):
        return self.value_type

    def is_truthy(self):
        raise NotImplementedError()

    def cast(self, new_type:ValueType):
        raise NotImplementedError()

    def get_value_object(self):
        raise NotImplementedError()

    @staticmethod
    def create(self, val):
        if isinstance(val, int) or isinstance(val, float):
            return IntValue(int(val))
        elif isinstance(val, float):
            return FloatValue(val)
        elif isinstance(val, str):
            return StringValue(val)
        elif isinstance(val, Path):
            return DivertTargetValue(val)
        else:
            return None

    def __init__(self, val=None):
        self.value = val or self.default_value()

    def __str__(self):
        return str(self.value)

class IntValue(Value):
    value_type = ValueType.INT

    def default_value(self):
        return 0
            
    def cast(self, new_type:ValueType):
        if new_type is ValueType.INT:
            return IntValue(self.value)
        elif new_type is ValueType.FLOAT:
            return FloatValue(float(self.value))
        elif new_type is ValueType.STRING:
            return StringValue(str(self.value))
        else:
            raise ValueError("Unexpected type cast of Value to new ValueType")

class FloatValue(Value):
    value_type = ValueType.FLOAT

    def default_value(self):
        return 0.0

    def cast(self, new_type:ValueType):
        if new_type is ValueType.INT:
            return IntValue(int(self.value))
        elif new_type is ValueType.FLOAT:
            return FloatValue(self.value)
        elif new_type is ValueType.STRING:
            return StringValue(str(self.value))
        else:
            raise ValueError("Unexpected type cast of Value to new ValueType")

class StringValue(Value):
    value_type = ValueType.STRING

    def default_value(self):
        return ""

    def cast(self, new_type:ValueType):
        if new_type is ValueType.INT:
            if self.value.isdigit():
                return IntValue(int(self.value))
            else:
                return None
        elif new_type is ValueType.FLOAT:
            try:
                return FloatValue(float(self.value))
            except ValueError:
                return None
        elif new_type is ValueType.STRING:
            return StringValue(self.value)
        else:
            raise ValueError("Unexpected type cast of Value to new ValueType")

class DivertTargetValue(Value):
    value_type = ValueType.DIVERT_TARGET

    def get_target_path(self):
        return self.value

    def set_target_path(self, path:Path):
        self.value = path
    
    def is_truthy(self):
        raise ValueError("Shouldn't be checking the truthiness of a divert target")

    def default_value(self):
        return None

    def cast(self, new_type:ValueType):
        if new_type == self.value_type:
            return DivertTargetValue(self.value)
        else:
            raise ValueError("Unexpected type cast of Value to new ValueType")

    def __str__(self):
        return "DivertTargetValue({})".format(self.get_target_path())

class VariablePointerValue(Value):
    value_type = ValueType.VARIABLE_POINTER
    UNDETERMINED_CONTEXT = -1
    GLOBAL_CONTEXT = 0

    def get_variable_name(self):
        return self.value
    
    def set_variable_name(self, name:str):
        self.value = name

    def is_truthy(self):
        raise ValueError("Shouldn't be checking the truthiness of a variable pointer")

    def get_context_index(self):
        return self.context_index

    def set_context_index(self, val):
        self.context_index = val
    
    def __init__(self, variable_name=None, context_index=None):
        super().__init__(variable_name)
        self.context_index = self.UNDETERMINED_CONTEXT if context_index is None else context_index

    def cast(self, new_type:ValueType):
        if new_type == self.value_type:
            return VariablePointerValue(self.value)
        else:
            raise ValueError("Unexpected type cast of Value to new ValueType")

