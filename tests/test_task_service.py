from ht.db import db
from ht.models.task import Task
from ht.services import task_service

title = 'title'
desc = 'desc'


def create_task():
    return task_service.create_task(title, desc)


def get_task(id):
    return task_service.get_by_id(id)


def test_crate_task():
    db.create_all()
    task_id = create_task()

    q_task = db.query(Task).get(task_id)
    assert q_task.title == title
    assert q_task.description == desc
    db.drop_all()


def test_add_time():
    db.create_all()
    task_id = create_task()
    task = get_task(task_id)

    minutes1 = 10
    desc1 = 'dummy description'

    task.start()
    task.add_time(minutes=minutes1, description=desc1)

    db.add(task)

    # commits the changes to db. Automatically expires the attributs
    db.commit()

    # refresh/un-expire the attars so that we can access them after the task
    # get's detached
    db.session.refresh(task)

    # detach all objects from the session
    db.session.expunge_all()

    db.session.remove()

    q_task = db.query(Task).get(task.id)
    assert q_task.title == task.title
    assert q_task.description == task.description
    assert len(q_task.times) == 1
    assert q_task.times[0].minutes == minutes1
    assert q_task.times[0].description == desc1
    assert q_task.description == task.description

    db.commit()
    db.session.remove()
