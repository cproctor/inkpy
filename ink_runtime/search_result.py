#  When looking up content within the story (e.g. in Container.ContentAtPath),
#  the result is generally found, but if the story is modified, then when loading
#  up an old save state, then some old paths may still exist. In this case we
#  try to recover by finding an approximate result by working up the story hierarchy
#  in the path to find the closest valid container. Instead of crashing horribly,
#  we might see some slight oddness in the content, but hopefully it recovers!

class SearchResult:
    def __init__(self, obj:'RuntimeObject', approximate:bool=False):
        self.obj = obj
        self.approximate = approximate

    def correct_object(self):
        return None if self.approximate else self.obj
