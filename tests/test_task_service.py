from ht.db import db
from ht.models.task import Task, TaskState
from ht.services import task_service

title = 'title'
desc = 'desc'


def create_task():
    return task_service.create_task(title, desc)


def get_task_by_id(id):
    return db.query(Task).get(id)


def test_crate_task():
    db.create_all()
    task_id = create_task()

    q_task = get_task_by_id(task_id)
    assert q_task.title == title
    assert q_task.description == desc
    db.drop_all()


def test_add_time():
    db.create_all()
    task_id = create_task()

    minutes1 = 10
    desc1 = 'dummy description'

    task_service.add_time(task_id, minutes1, desc1)

    q_task = get_task_by_id(task_id)
    assert len(q_task.times) == 1
    assert q_task.times[0].minutes == minutes1
    assert q_task.times[0].description == desc1
    db.drop_all()


def test_start_task():
    db.create_all()
    task_id = create_task()
    task_service.start_task(task_id)
    q_task = get_task_by_id(task_id)
    assert q_task.state == TaskState.IN_PROGRESS
    db.drop_all()


def test_complete_task():
    db.create_all()
    task_id = create_task()
    task_service.start_task(task_id)
    task_service.complete_task(task_id)
    q_task = get_task_by_id(task_id)
    assert q_task.state == TaskState.COMPLETED
    db.drop_all()
