from ht.db import db
from .task import TaskService

task_service = TaskService(db)
