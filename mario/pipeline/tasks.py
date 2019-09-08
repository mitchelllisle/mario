from uuid import uuid4
import datetime as dt
from typing import Callable


class Task:
    def __init__(self, instance: Callable, description: str, depends_on: Callable = None):
        self.status = "PENDING"
        self.description = description
        self._func = instance
        self.task_id = str(uuid4())
        self.task_name = instance.__name__
        self.task_started = None
        self.task_ended = None
        self.task_duration_milliseconds = None
        self.output = {"data": None, "logs": None, "errors": None}
        self.depends_on = None if depends_on is None else depends_on.task_name

    def as_dict(self):
        output = {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_started": self.task_started,
            "task_ended": self.task_ended,
            "task_duration_milliseconds": self.task_duration_milliseconds,
            "status": self.status,
            "output": self.output,
            "depends_on": self.depends_on
        }
        return output

    def run_task(self, **kwargs):
        task_start = dt.datetime.now()
        try:
            self.status = "RUNNING"
            self.task_started = task_start.isoformat()
            self.output['data'] = self._func(**kwargs)
            self.status = "SUCCEEDED"
        except Exception as err:
            self.status = "FAILED"
            self.output['errors'] = str(err)
        finally:
            task_end = dt.datetime.now()
            self.task_ended = task_end.isoformat()
            self.task_duration_milliseconds = (
                    (task_end - task_start).microseconds / 1000
            )
            return self.as_dict()
