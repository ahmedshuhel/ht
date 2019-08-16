from sqlalchemy import Table, Column,\
    Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship

from h.models.task import Task, Time
from h.models.list import List
from h.models.board import Board

from .database import Database


db = Database()

board_metadata = Table(
    'board', db.metadata,
    Column('id', String, primary_key=True),
    Column('title', String(100)),
    Column('description', String(250)),
    Column('created_at', DateTime)
)

task_metadata = Table(
    'task', db.metadata,
    Column('id', String, primary_key=True),
    Column('title', String(100)),
    Column('description', String(250)),
    Column('state', Integer),
    Column('created_at', DateTime)
)

time_metadata = Table(
    'time', db.metadata,
    Column('id', String, primary_key=True),
    Column('minutes', Integer),
    Column('description', String(250)),
    Column('task_id', Integer, ForeignKey('task.id'))
)

task_list_table = Table(
    'list_task', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('list_id', Integer, ForeignKey('list.id')),
    Column('task_id', Integer, ForeignKey('task.id'))
)

board_list_table = Table(
    'board_list', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('board_id', Integer, ForeignKey('board.id')),
    Column('list_id', Integer, ForeignKey('list.id'))
)


list_metadata = Table(
    'list', db.metadata,
    Column('id', String, primary_key=True),
    Column('title', String(100)),
    Column('created_at', DateTime)
)

mapper(List, list_metadata, properties={
    'tasks': relationship(Task, secondary=task_list_table),
    'board': relationship(
        Board, secondary=board_list_table, back_populates='lists'
    )
})

mapper(Board, board_metadata, properties={
    'lists': relationship(List, secondary=board_list_table)
})

mapper(Task, task_metadata, properties={
    'times': relationship(Time),
    'list': relationship(
        List, secondary=task_list_table, back_populates='tasks'
    )
})

mapper(Time, time_metadata)
