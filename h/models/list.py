from .base import Base


class ListError(Exception):
    pass


class List(Base):
    BACKLOG = 'Backlog'

    def __init__(self, title):
        super(List, self).__init__()
        self.title = title
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    @classmethod
    def create_backlog(cls):
        return List(cls.BACKLOG)

