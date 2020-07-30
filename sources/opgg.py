from sources import Source


class Opgg(Source):

    def __init__(self):
        """ Implements op.gg as a source """
        super().__init__("opgg")

    def get_champions(self):
        raise NotImplementedError

    def get_items(self, champion, role):
        raise NotImplementedError

    def get_skill_order(self, champion, role):
        raise NotImplementedError

    def get_version(self):
        raise NotImplementedError
