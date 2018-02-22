from pytest import fixture
from ht.db import db


@fixture(autouse=True)
def db_fixture():
    db.create_all()
    yield db
    db.drop_all()

