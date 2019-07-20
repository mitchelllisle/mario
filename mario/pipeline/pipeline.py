from uuid import uuid4
import datetime as dt
from typing import Text, Callable, Dict
from mario.pipeline.tasks import Task
from mario.pipeline.utils import Output


class Pipeline:
    def __init__(self, description: Text = None, hide_output=None):
        """
        Pipeline
        This is a simple implementation currently that creates a list
        of tasks to run in sequence. The order is determined by tasks that
        'depend on' other tasks.
        """
        self.tasks = []
        self.pipeline_id = str(uuid4())
        self.description = description
        self.pipeline_created = dt.datetime.now().isoformat()
        self.task_outputs = []

    @property
    def SUCCEEDED(self):
        self.status = "SUCCEEDED"

    @property
    def RUNNING(self):
        self.status = "RUNNING"

    @property
    def FAILED(self):
        self.status = "FAILED"

    def collect_output(self):
        output = {
            "pipeline_id": self.pipeline_id,
            "total_tasks": self.total_tasks,
            "description": self.description,
            "pipeline_created": self.pipeline_created,
            "pipeline_started": self.pipeline_started,
            "pipeline_ended`": self.pipeline_ended,
            "pipeline_duration_milliseconds": self.pipeline_duration_milliseconds,
            "status": self.status,
            "task_outputs": self.task_outputs
        }
        return output

    def task(self, depends_on: Text = None, description: Text = None):
        """
        A task represents a single piece of a pipeline to be executed. A task
        should be kept as small as possible.
        Example:
            @pipe.task()
            def one(val, val2):
                return val + val2


            @pipe.task(depends_on=one)
            def two(val):
                return val + 1
        """
        order_in_pipeline = 0
        if depends_on:
            order_in_pipeline = self.tasks.index(depends_on) + 1

        def build_function(instance: Callable) -> Dict:
            func_meta = Task(instance)

            self.tasks.insert(order_in_pipeline, func_meta)
            return func_meta
        return build_function

    def run(self, config: Dict):
        try:
            def build_config(task_config: Dict) -> Dict:
                parsed_config = {}
                if task_config is not None:
                    for arg, val in task_config.items():
                        if type(val) is Output:
                            parsed_config[arg] = val.get_output()
                        else:
                            parsed_config[arg] = val
                return parsed_config

            total_tasks = len(self.tasks)
            pipeline_start = dt.datetime.now()

            self.total_tasks = total_tasks
            self.pipeline_started = pipeline_start.isoformat()

            for i in range(total_tasks):
                parsed_config = build_config(
                    task_config=config[self.tasks[i].task_name]
                )

                self.task_outputs.append(self.tasks[i].run_task(**parsed_config))

            pipeline_end = dt.datetime.now()
            self.pipeline_ended = pipeline_end.isoformat()
            self.pipeline_duration_milliseconds = (
                ((pipeline_end - pipeline_start).microseconds) / 1000
            )
            self.SUCCEEDED
        except Exception:
            self.FAILED
            self.error_caused_by = self.tasks[i].task_name
            raise
        return self.collect_output()
