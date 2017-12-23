from ht.models.task import Task, TaskState


class TaskService(object):
    def __init__(self, db):
        self.db = db

    def get_by_id(self, id):
        return self.db.query(Task).get(id)

    def create_task(self, title, description):
        task = Task(title, description)
        self.db.add(task)
        task_id = task.id
        self.db.save_changes()
        return task_id

    def add_time(self, task_id, minutes, description=None):
        task = self.get_by_id(task_id)
        if task.state < TaskState.IN_PROGRESS:
            task.start()

        task.add_time(minutes, description)
        self.db.save_changes()

    def start_task(self, task_id):
        task = self.get_by_id(task_id)
        task.start()
        self.db.save_changes()

    def complete_task(self, task_id):
        task = self.get_by_id(task_id)
        task.complete()
        self.db.save_changes()
