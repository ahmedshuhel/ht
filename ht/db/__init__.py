from ht.models.task import Task, Time
from sqlalchemy import Table, Column,\
     Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship

from .ht_database import Database


db = Database()

task_metadata = Table(
    'task', db.metadata,
    Column('id', String, primary_key=True),
    Column('title', String(100)),
    Column('description', String(250)),
    Column('state', String(50)),
    Column('created_at', DateTime)
)

time_metadata = Table(
    'time', db.metadata,
    Column('id', String, primary_key=True),
    Column('minutes', Integer),
    Column('description', String(250)),
    Column('task_id', Integer, ForeignKey('task.id'))
)


mapper(Task, task_metadata, properties={
    'times': relationship(Time)
})

mapper(Time, time_metadata)
