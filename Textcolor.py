#class used for formating text 
class Text_colors:
    def __init__(self):
        self._YELLOW = '\033[93m'
        self._RED = '\033[91m'
        self._NORMAL = '\033[0m'

    def make_yellow(self, data):
        return self._YELLOW + f"{data}" + self._NORMAL 

    def make_red(self, data):
        return self._RED + f"{data}" + self._NORMAL