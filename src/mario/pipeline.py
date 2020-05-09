from mario.registry import Registry
from typing import List
from uuid import uuid4
from mario.funcs import FnConfig


class Pipeline:
    def __init__(self, registry: Registry):
        self._id = str(uuid4())
        self._registry = registry
        self._configs = None
        self._time_started = None
        self._time_ended = None
        self._status = "NOT STARTED"
        self._steps = []
        self.results = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.determine_status()
        self.results = self.collect_output()

    def determine_status(self):
        #  ToDo: Implement way of capturing overall pipeline status
        pass

    def collect_output(self):
        return {
            "id": self._id,
            "status": self._status,
            "steps": self._steps
        }

    def run(self, config: List[FnConfig]):
        self._configs = config
        for config in self._configs:
            func = self._registry[config.fn]
            f = func(config.name)
            f(**config.args)
            self._steps.append(f.collect_output())

