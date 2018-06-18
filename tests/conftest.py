from pytest import fixture
from ht.db import db
from ht.api import task_api


@fixture(autouse=True)
def db_fixture():
    db.create_all()
    task_api.create_backlog()
    yield
    db.drop_all()
