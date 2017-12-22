from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class Database(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.metadata = MetaData()

    @property
    def query(self):
        return self.session.query

    def add(self, *args, **kwargs):
        return self.session.add(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    def flush(self, *args, **kwargs):
        return self.session.flush(*args, **kwargs)

    def commit(self, *args, **kwargs):
        return self.session.commit(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        return self.session.rollback(*args, **kwargs)

    def create_all(self, *args, **kwargs):
        kwargs.setdefault('bind', self.engine)
        self.metadata.create_all(*args, **kwargs)

    def drop_all(self, *args, **kwargs):
        kwargs.setdefault('bind', self.engine)
        self.metadata.drop_all(*args, **kwargs)
