from unittest import TestCase
from ink_runtime.path import Component, Path
from ink_runtime.value import ValueType, IntValue, FloatValue, StringValue, DivertTargetValue, VariablePointerValue

class TestIntValue(TestCase):
    def setUp(self):
        self.default = IntValue()
        self.four = IntValue(4)

    def test_default(self):
        self.assertEqual(self.default.value, 0)

    def test_constructor(self):
        self.assertEqual(self.four.value, 4)

    def test_cast(self):
        self.assertEqual(self.four.cast(ValueType.FLOAT).value, 4.0)
        self.assertEqual(self.four.cast(ValueType.STRING).value, "4")

class TestFloatValue(TestCase):
    def setUp(self):
        self.default = FloatValue()
        self.half = FloatValue(0.5)

    def test_default(self):
        self.assertEqual(self.default.value, 0.0)

    def test_constructor(self):
        self.assertEqual(self.half.value, 0.5)

    def test_cast(self):
        self.assertEqual(self.half.cast(ValueType.INT).value, 0)
        self.assertEqual(self.half.cast(ValueType.STRING).value, "0.5")

class TestStringValue(TestCase):
    def setUp(self):
        self.default = StringValue()
        self.funny = StringValue("joke")

    def test_default(self):
        self.assertEqual(self.default.value, "")

    def test_constructor(self):
        self.assertEqual(self.funny.value, "joke")

    def test_cast(self):
        self.assertEqual(self.funny.cast(ValueType.INT), None)
        self.assertEqual(self.funny.cast(ValueType.FLOAT), None)
        self.assertEqual(StringValue("12").cast(ValueType.INT).value, 12)
        self.assertEqual(StringValue("0.234").cast(ValueType.FLOAT).value, 0.234)

class TestDivertTargetValue(TestCase):
    def setUp(self):
        self.path = Path(components_string="this.that.0.1")
        self.null_dt = DivertTargetValue()
        self.dt = DivertTargetValue(self.path)

    def test_get_target_path(self):
        self.assertEqual(self.dt.get_target_path(), self.path)
        self.assertEqual(self.null_dt.get_target_path(), None)

    def test_set_target_path(self):
        self.null_dt.set_target_path(self.path)
        self.assertEqual(self.null_dt.get_target_path(), self.path)

    def test_default_value_is_none(self):
        self.assertIs(self.null_dt.value, None)

class TestVariablePointerValue(TestCase):
    pass

        
        
    

if __name__ == '__main__':
    unittest.main()

