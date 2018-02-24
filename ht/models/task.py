from datetime import datetime
from .base import Base


class TaskError(Exception):
    pass


class TaskState:
    INIT = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class Time(Base):
    def __init__(self, minutes, description):
        super(Time, self).__init__()
        self.minutes = minutes
        self.description = description


class Task(Base):
    def __init__(self, title, description, list):
        super(Task, self).__init__()
        self.title = title
        self.description = description
        self.state = TaskState.INIT
        self.list = list
        self.times = []

    def update_description(self, description):
        self.description = description

    def start(self):
        if self.state != TaskState.INIT:
            raise TaskError(
                'Cannot start a task in `{}` state'.format(self.state)
            )

        self.state = TaskState.IN_PROGRESS
        self.start_time = datetime.now()

    def complete(self):
        if self.state != TaskState.IN_PROGRESS:
            raise TaskError('Cannot complete a task without starting it')

        self.state = TaskState.COMPLETED
        self.end_time = datetime.now()

    def add_time(self, minutes, description):
        if self.state != TaskState.IN_PROGRESS:
            raise TaskError(
                'Cannot add time for the task in `{}` state'.format(self.state)
            )

        self.times.append(Time(minutes, description))

    @property
    def total_time(self):
        return sum(time.minutes for time in self.times)
