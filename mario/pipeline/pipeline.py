from uuid import uuid4
import datetime as dt
from typing import Text, Callable, Dict
from mario.pipeline.tasks import Task
from mario.pipeline.utils import Output


class Pipeline:
    def __init__(self, description: Text = None):
        """
        Pipeline
        This is a simple implementation currently that creates a list
        of tasks to run in sequence. The order is determined by tasks that
        'depend on' other tasks.
        """
        self.status = "PENDING"
        self.tasks = []
        self.pipeline_id = str(uuid4())
        self.description = description
        self.pipeline_created = dt.datetime.now().isoformat()
        self.pipeline_started = "Not Started"
        self.pipeline_ended = "Not Started"
        self.total_tasks = 0
        self.error_caused_by = None
        self.pipeline_duration_milliseconds = 0

    def as_dict(self):
        output = {
            "pipeline_id": self.pipeline_id,
            "total_tasks": self.total_tasks,
            "description": self.description,
            "pipeline_created": self.pipeline_created,
            "pipeline_started": self.pipeline_started,
            "pipeline_ended": self.pipeline_ended,
            "pipeline_duration_milliseconds": self.pipeline_duration_milliseconds,
            "status": self.status,
            "tasks": [x.as_dict() for x in self.tasks]
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

        def build_function(instance: Callable) -> Task:
            func_meta = Task(instance=instance, description=description, depends_on=depends_on)

            self.tasks.insert(order_in_pipeline, func_meta)
            self.total_tasks += 1
            return func_meta
        return build_function

    def run(self, config: Dict):
        def build_config(task_config: Dict) -> Dict:
            working_config = {}
            if task_config is not None:
                for arg, val in task_config.items():
                    if type(val) is Output:
                        working_config[arg] = val.get_output()
                    else:
                        working_config[arg] = val
            return working_config

        pipeline_start = dt.datetime.now()
        self.pipeline_started = pipeline_start.isoformat()

        for i in range(self.total_tasks):
            parsed_config = build_config(
                task_config=config[self.tasks[i].task_name]
            )

            output_from_task = self.tasks[i].run_task(**parsed_config)
            if output_from_task['status'] == "SUCCEEDED":
                self.status = "SUCCEEDED"
                continue
            else:
                self.status = "FAILED"
                self.error_caused_by = self.tasks[i].task_name
                break

        pipeline_end = dt.datetime.now()
        self.pipeline_ended = pipeline_end.isoformat()
        self.pipeline_duration_milliseconds = (
                (pipeline_end - pipeline_start).microseconds / 1000
        )
        return self.as_dict()
