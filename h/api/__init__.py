from h.db import db
from .task_api import TaskApi

task_api = TaskApi(db)
