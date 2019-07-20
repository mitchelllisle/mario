from uuid import uuid4
import datetime as dt
from typing import Callable


class Task:
    def __init__(self, instance: Callable, depends_on=None):
        self._func = instance
        self.task_id = str(uuid4())
        self.task_name = instance.__name__
        self.status = None
        self.output = {"data": None, "logs": None, "errors": None}
        self.depends_on = None

    @property
    def SUCCEEDED(self):
        self.status = "SUCCEEDED"

    @property
    def RUNNING(self):
        self.status = "RUNNING"

    @property
    def PENDING(self):
        self.status = "PENDING"

    @property
    def FAILED(self):
        self.status = "FAILED"

    def collect_output(self):
        output = {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_depends_on": self.depends_on,
            "status": self.status,
            "task_started": self.task_started,
            "task_ended": self.task_ended,
            "task_duration_milliseconds": self.task_duration_milliseconds,
            "output": self.output
        }
        return output

    def run_task(self, **kwargs):
        try:
            self.RUNNING
            task_start = dt.datetime.now()
            self.task_started = task_start.isoformat()
            self.output['data'] = self._func(**kwargs)
            self.SUCCEEDED
        except Exception as e:
            self.FAILED
            self.output['errors'] = e
        finally:
            task_end = dt.datetime.now()
            self.task_ended = task_end.isoformat()
            self.task_duration_milliseconds = (
                ((task_end - task_start).microseconds) / 1000
            )
            return self.collect_output()
