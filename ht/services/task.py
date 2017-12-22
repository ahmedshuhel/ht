from ht.models.task import Task, Time


class TaskService(object):
    def __init__(self, db):
        self.db = db

    def get_by_id(self, id):
        return self.db.query(Task).get(id)

    def create_task(self, title, description):
        task = Task(title, description)
        self.db.add(task)
        self.db.save_changes()

    def add_time(self, task_id, minutes, description=None):
        task = self.get_by_id(task_id)
        task.add_time(Time(minutes, description))
