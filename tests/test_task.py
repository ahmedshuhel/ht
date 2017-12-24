import mock
import pytest
from ht.models.task import Task, TaskState, TaskError
from datetime import datetime


title = 'This is a new task'
desc = 'This is description'
created_at = datetime.min


def create_task():
    return Task(
        title=title,
        description=desc
    )


@mock.patch('ht.models.base.uuid4')
def test_create_task(mock_uuid4):
    uuid = 'a1b2c3'
    mock_uuid4.return_value = uuid
    task = create_task()
    assert task.title == title
    assert task.description == desc
    assert task.state == TaskState.INIT
    assert task.id == uuid


@mock.patch('ht.models.base.datetime')
def test_has_created_at(mock_datetime):
    mock_datetime.now.return_value = datetime.min
    task = create_task()
    assert task.created_at == created_at


def test_update_description():
    desc = 'Fake description'
    task = create_task()
    task.update_description(desc)
    assert task.description == desc


def test_start_woring_on():
    task = create_task()
    task.start()
    assert task.state == TaskState.IN_PROGRESS


@mock.patch('ht.models.task.datetime')
def test_record_start_time(mock_datetime):
    mock_datetime.now.return_value = datetime.min
    task = create_task()
    task.start()
    assert task.start_time == datetime.min


def test_complete_task():
    task = create_task()
    task.start()
    task.complete()
    assert task.state == TaskState.COMPLETED


@mock.patch('ht.models.task.datetime')
def test_record_end_time(mock_datetime):
    mock_datetime.now.return_value = datetime.min
    task = create_task()
    task.start()
    task.complete()
    assert task.end_time == datetime.min


def test_throw_if_start_a_not_init_task():
    task = create_task()
    with pytest.raises(TaskError) as err:
        task.start()
        task.complete()
        task.start()
    assert str(err.value) == 'Cannot start a task in `{}` state'.format(
        TaskState.COMPLETED
    )


def test_throw_if_complete_without_starting():
    task = create_task()
    with pytest.raises(TaskError) as err:
        task.complete()
    assert str(err.value) == 'Cannot complete a task without starting it'


def test_times_is_empty_after_task_creation():
    task = create_task()
    assert len(task.times) == 0


def test_add_time():
    minutes1 = 10
    minutes2 = minutes1 + 5
    desc1 = 'dummy description'
    desc2 = desc1 + 'dummy description'
    task = create_task()
    task.start()

    task.add_time(minutes=minutes1, description=desc1)
    task.add_time(minutes=minutes2, description=desc2)

    assert task.times[0].minutes == minutes1
    assert task.times[0].description == desc1
    assert task.times[1].minutes == minutes2
    assert task.times[1].description == desc2
    assert task.total_time == minutes1 + minutes2
