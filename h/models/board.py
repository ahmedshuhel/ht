from .base import Base


class BoardError(Exception):
    pass


class Board(Base):

    def __init__(self, title, description):
        super(Board, self).__init__()
        self.title = title
        self.description = description
        self.lists = []

    def add_list(self, list):
        self.lists.append(list)

    def remove_list(self, list):
        self.lists.remove(list)
