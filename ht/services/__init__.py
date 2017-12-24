from ht.db import db
from .task import TaskService
from .list import ListService

task_service = TaskService(db)
list_service = ListService(db, task_service)
