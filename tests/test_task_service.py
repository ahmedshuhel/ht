from ht.models.task import Task
from ht.db import db


def test_persist_task_with_all_attributes():
    db.create_all()

    minutes1 = 10
    minutes2 = minutes1 + 5
    desc1 = 'dummy description'
    desc2 = desc1 + 'dummy description'
    task = Task('A new task')
    task.start()
    task.add_time(minutes=minutes1, description=desc1)
    task.add_time(minutes=minutes2, description=desc2)

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
    assert len(q_task.times) == 2
    assert q_task.times[0].minutes == minutes1
    assert q_task.times[1].minutes == minutes2
    assert q_task.times[0].description == desc1
    assert q_task.times[1].description == desc2
    assert q_task.description == task.description

    db.commit()
    db.session.remove()
