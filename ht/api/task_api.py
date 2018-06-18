from ht.models.list import List
from ht.models.task import Task, TaskState


class TaskApi(object):
    def __init__(self, db):
        self.db = db

    @property
    def backlog_id(self):
        return self.get_backlog().id

    def get_task_by_id(self, id):
        return self.db.query(Task).get(id)

    def _create_task(self, title, description):
        task = Task(title, description)
        self.db.add(task)
        task_id = task.id
        return task_id

    def create_task(self, title, description):
        task_id = self._create_task(title, description)
        self._add_to_list(self.backlog_id, task_id)
        self.db.save_changes()
        return task_id

    def add_time(self, task_id, minutes, description=None):
        task = self.get_task_by_id(task_id)
        if task.state < TaskState.IN_PROGRESS:
            task.start()

        task.add_time(minutes, description)
        self.db.save_changes()

    def start_task(self, task_id):
        task = self.get_task_by_id(task_id)
        task.start()
        self.db.save_changes()

    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        task.complete()
        self.db.save_changes()

    def create_list(self, title):
        list = List(title)
        self.db.add(list)
        list_id = list.id
        self.db.save_changes()
        return list_id

    def create_backlog(self):
        list = List.create_backlog()
        self.db.add(list)
        list_id = list.id
        self.db.save_changes()
        return list_id

    def get_backlog(self):
        return self.db.query(List).filter(List.title == List.BACKLOG).one()

    def get_list_by_id(self, id):
        return self.db.query(List).get(id)

    def add_to_list(self, list_id, task_id):
        self._add_to_list(list_id, task_id)
        self.db.save_changes()

    def _add_to_list(self, list_id, task_id):
        list = self.get_list_by_id(list_id)
        task = self.db.query(Task).get(task_id)
        list.add_task(task)
