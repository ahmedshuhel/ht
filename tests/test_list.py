import mock

from datetime import datetime
from h.models.task import Task
from h.models.list import List


title = 'This is a new task'
desc = 'This is description'
created_at = datetime.min


def create_task():
    return Task(
        title=title,
        description=desc
    )


def create_list():
    return List(title=title)


@mock.patch('h.models.base.uuid4')
def test_create_list(mock_uuid4):
    uuid = 'a1b2c3'
    mock_uuid4.return_value = uuid
    list = create_list()
    assert list.title == title
    assert list.id == uuid


@mock.patch('h.models.base.datetime')
def test_has_created_at(mock_datetime):
    mock_datetime.now.return_value = datetime.min
    list = create_list()
    assert list.created_at == created_at


def test_add_task():
    list = create_list()
    task = create_task()

    list.add_task(task)

    assert len(list.tasks) == 1
    assert list.tasks[0].title == title
    assert list.tasks[0].description == desc
