from unittest import TestCase
from ink_runtime.debug_metadata import DebugMetadata

class TestDebugMetadata(TestCase):
    def test_str(self):
        dm = DebugMetadata()
        self.assertEqual(str(dm), "line 0")
        dm.start_line_number = 12
        dm.file_name = "file.txt"
        self.assertEqual(str(dm), "line 12 of file.txt")

if __name__ == '__main__':
    unittest.main()
