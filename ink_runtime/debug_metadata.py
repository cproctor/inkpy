from typing import Optional

class DebugMetadata:
    def __init__(self, start_line_number:int=0, end_line_number:int=0,
            file_name:Optional[str]=None, source_name:Optional[str]=None):
        self.start_line_number = start_line_number
        self.end_line_number = end_line_number
        self.file_name = file_name
        self.source_name = source_name
    
    # Seems incomplete?
    def __str__(self) -> str:
        if self.file_name is not None:
            return "line {} of {}".format(self.start_line_number, self.file_name)
        else:
            return "line {}".format(self.start_line_number)
