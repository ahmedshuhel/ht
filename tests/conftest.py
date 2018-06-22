from pytest import fixture
from h.db import db
from h.api import task_api


@fixture(autouse=True)
def db_fixture():
    db.create_all()
    task_api.create_backlog()
    yield
    db.drop_all()
