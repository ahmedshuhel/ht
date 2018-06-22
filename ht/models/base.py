from uuid import uuid4
from datetime import datetime


class Base(object):
    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now()

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Base):
            return self.id == other.id
        return False

