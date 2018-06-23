from h.models.list import List
from h.models.board import Board
from h.models.task import Task, TaskState


class TaskApi(object):
    def __init__(self, db):
        self.db = db

    @property
    def backlog_id(self):
        return self.get_backlog().id

    def get_task_by_id(self, id):
        return self.db.query(Task).get(id)

    def get_board_by_id(self, id):
        return self.db.query(Board).get(id)

    def get_backlog(self):
        return self.db.query(List).filter(List.title == List.BACKLOG).one()

    def get_list_by_id(self, id):
        return self.db.query(List).get(id)

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

    def add_to_list(self, list_id, task_id):
        self._add_to_list(list_id, task_id)
        self.db.save_changes()

    def _add_to_list(self, list_id, task_id):
        list = self.get_list_by_id(list_id)
        task = self.db.query(Task).get(task_id)
        list.add_task(task)

    def _remove_from_list(self, list_id, task_id):
        list = self.get_list_by_id(list_id)
        task = self.db.query(Task).get(task_id)
        list.remove_task(task)

    def remove_from_list(self, list_id, task_id):
        self._remove_from_list(list_id, task_id)
        self.db.save_changes()

    def move_task(self, from_list_id, to_list_id, task_id):
        self._remove_from_list(from_list_id, task_id)
        self._add_to_list(to_list_id, task_id)
        self.db.save_changes()

    def create_board(self, title, description=''):
        board = Board(title, description)
        self.db.add(board)
        board_id = board.id
        self.db.save_changes()
        return board_id

    def add_to_board(self, board_id, list_id):
        board = self.get_board_by_id(board_id)
        list = self.get_list_by_id(list_id)
        board.add_list(list)
        self.db.save_changes()

    def remove_from_board(self, board_id, list_id):
        board = self.get_board_by_id(board_id)
        list = self.get_list_by_id(list_id)
        board.remove_list(list)
        self.db.save_changes()
