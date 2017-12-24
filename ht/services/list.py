from ht.models.list import List


class ListService(object):
    def __init__(self, db, task_svc):
        self.db = db
        self.task_svc = task_svc

    def create_list(self, title):
        list = List(title)
        self.db.add(list)
        list_id = list.id
        self.db.save_changes()
        return list_id

    def get_by_id(self, id):
        return self.db.query(List).get(id)

    def add_task(self, list_id, task_id):
        list = self.get_by_id(list_id)
        task = self.task_svc.get_by_id(task_id)
        list.add_task(task)
        self.db.save_changes()
