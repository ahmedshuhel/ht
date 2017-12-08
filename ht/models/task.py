from datetime import datetime


class TaskError(Exception):
    pass


class TaskState:
    INIT = 'init'
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'


class Time:
    def __init__(self, minutes, description):
        self.minutes = minutes
        self.description = description


class Task:
    def __init__(self, title):
        self.title = title
        self.created_at = datetime.now()
        self.description = ''
        self.state = TaskState.INIT
        self.times = []

    def add_description(self, description):
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
