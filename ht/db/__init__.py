from ht.models.task import Task, Time
from sqlalchemy import Table, MetaData, Column,\
     Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

metadata = MetaData()

task_metadata = Table(
    'task', metadata,
    Column('id', String, primary_key=True),
    Column('title', String(100)),
    Column('description', String(250)),
    Column('state', String(50)),
    Column('created_at', DateTime)
)

time_metadata = Table(
    'time', metadata,
    Column('id', String, primary_key=True),
    Column('minutes', Integer),
    Column('description', String(250)),
    Column('task_id', Integer, ForeignKey('task.id'))
)


mapper(Task, task_metadata, properties={
    'times': relationship(Time)
})

mapper(Time, time_metadata)

engine = create_engine('sqlite:///:memory:', echo=True)
metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))
