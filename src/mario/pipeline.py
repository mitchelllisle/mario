from mario.registry import Registry
from typing import List, Union, Type
from uuid import uuid4
from mario.funcs import FnConfig, DoFn
from mario.util import Status


class Pipeline:
    def __init__(self, registry: Registry):
        self.id = str(uuid4())
        self._registry = registry
        self._configs = None
        self.time_started = None
        self.time_ended = None
        self.status = "NOT STARTED"
        self.steps = []
        self.result = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.determine_status()
        self.result = self.collect_output()

    def determine_status(self):
        statuses = [step["status"] for step in self.steps]
        if any(x == Status.FAIL for x in statuses):
            self.status = Status.FAIL
        elif all(x == Status.SUCCEESS for x in statuses):
            self.status = Status.SUCCEESS

    def collect_output(self):
        return {
            "id": self.id,
            "status": self.status,
            "steps": self.steps
        }

    def _resolve_fn_location(self, fn: Union[str, Type[DoFn]]):
        if isinstance(fn, str):
            return self._registry[fn]
        elif issubclass(fn, DoFn):
            return fn

    def run(self, config: List[FnConfig]):
        self._configs = config
        for config in self._configs:
            func = self._resolve_fn_location(config.fn)
            f = func(config.name)
            try:
                f(**config.args)
            except:
                pass
            self.steps.append(f.collect_output())
