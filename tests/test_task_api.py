from h.db import db
from h.models.task import Task, TaskState
from h.models.list import List
from h.api import task_api as api

title = 'title'
desc = 'desc'


def create_task():
    return api.create_task(title, desc)


def create_list(title='list title'):
    return api.create_list(title)


def get_task_by_id(id):
    return db.query(Task).get(id)


def get_list(id):
    return db.query(List).get(id)


def test_create_list():
    list_id = create_list()
    list = get_list(list_id)
    assert list.title == 'list title'


def test_create_task():
    task_id = create_task()

    q_task = get_task_by_id(task_id)
    assert q_task.title == title
    assert q_task.description == desc


def test_add_task_to_list():
    task_id = create_task()
    list_id = create_list()
    api.add_to_list(list_id, task_id)

    list = get_list(list_id)
    assert len(list.tasks) == 1
    assert list.tasks[0].title == 'title'
    assert list.tasks[0].description == 'desc'


def test_remove_task_from_list():
    task_id = create_task()
    list_id = create_list()
    api.add_to_list(list_id, task_id)

    list = get_list(list_id)
    assert len(list.tasks) == 1
    assert list.tasks[0].title == 'title'

    api.remove_from_list(list_id, task_id)
    list = get_list(list_id)
    assert len(list.tasks) == 0


def test_task_to_be_in_backlog_on_creation():
    backlog_id = api.backlog_id
    task_id = create_task()
    task = get_task_by_id(task_id)
    assert backlog_id in [task_list.id for task_list in task.list]


def test_task_can_be_moved_from_one_list_to_another():
    backlog_id = api.backlog_id
    task_id = create_task()
    todo_list_id = create_list('todo')
    api.move_task(backlog_id, todo_list_id, task_id)
    task = get_task_by_id(task_id)
    task_list_ids = [task_list.id for task_list in task.list]
    assert backlog_id not in task_list_ids
    assert todo_list_id in task_list_ids


def test_add_time():
    task_id = create_task()

    minutes1 = 10
    desc1 = 'dummy description'

    api.add_time(task_id, minutes1, desc1)

    q_task = get_task_by_id(task_id)
    assert len(q_task.times) == 1
    assert q_task.times[0].minutes == minutes1
    assert q_task.times[0].description == desc1


def test_start_task():
    task_id = create_task()
    api.start_task(task_id)
    q_task = get_task_by_id(task_id)
    assert q_task.state == TaskState.IN_PROGRESS


def test_complete_task():
    task_id = create_task()
    api.start_task(task_id)
    api.complete_task(task_id)
    q_task = get_task_by_id(task_id)
    assert q_task.state == TaskState.COMPLETED
