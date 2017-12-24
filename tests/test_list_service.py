from ht.db import db
from ht.models.list import List
from ht.services import list_service, task_service

title = 'title'


def create_task():
    return task_service.create_task('title', 'desc')


def create_list():
    return list_service.create_list(title)


def get_list(id):
    return db.query(List).get(id)


def test_crate_list():
    db.create_all()
    list_id = create_list()

    list = get_list(list_id)
    assert list.title == title
    db.drop_all()


def test_add_task():
    db.create_all()
    task_id = create_task()
    list_id = create_list()
    list_service.add_task(list_id, task_id)

    list = get_list(list_id)
    assert len(list.tasks) == 1
    assert list.tasks[0].title == 'title'
    assert list.tasks[0].description == 'desc'
    db.drop_all()
