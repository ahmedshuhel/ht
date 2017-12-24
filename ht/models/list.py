from .base import Base


class ListError(Exception):
    pass


class List(Base):
    def __init__(self, title):
        super(List, self).__init__()
        self.title = title
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
