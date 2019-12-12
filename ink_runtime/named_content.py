
# Migration of INamedContent
class NamedContentMixin:
    name = ""
    def has_valid_name(self):
        return False

