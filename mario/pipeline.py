from uuid import uuid4
import datetime as dt


class Pipeline:
    def __init__(self, description=None):
        """
        Pipeline
        This is a simple implementation currently that creates a list
        of tasks to run in sequence. The order is determined by tasks that 'depend on' other tasks.
        """
        self.tasks = []
        self.description = description

    def task(self, depends_on=None, description=None):
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
        idx = 0
        if depends_on:
            idx = self.tasks.index(depends_on) + 1

        def build_function(instance):
            func_meta = {
                "task_id": str(uuid4()),
                "function_name": instance.__name__,
                "function_code": instance,
                "status": "PENDING",
                "output": None
            }
            self.tasks.insert(idx, func_meta)
            return func_meta
        return build_function

    def clear(self):
        """
        Remove all tasks from a Pipeline. TODO: allow the ability to clear
        single tasks from a pipeline.
        """
        self.tasks = []

    def run(self, config):
        """
        Example:
            config = {
                "one": {
                    "val": 1,
                    "val2": 1
                },
                "two": {
                    "val": 2
                }
            }
            pipe.run(config)

        Returns:
            {'total_tasks': 2,
             'pipeline_id': '9381b42f-147f-4c8d-908b-4ab7f3f73c64',
             'started': datetime.datetime(2019, 7, 8, 22, 13, 3, 981497),
             'tasks': [
                {
                    'task_id': 'e28f4ba4-d392-4ffc-bd0e-d1b43d1bff0a',
                    'function_name': 'uno',
                    'function_code': <function __main__.uno(uno)>,
                    'status': 'SUCCEEDED',
                    'output': 'this is 1',
                    'started': datetime.datetime(2019, 7, 8, 22, 13, 3, 981508),
                    'ended': datetime.datetime(2019, 7, 8, 22, 13, 3, 981515),
                    'total_duration_seconds': 7e-06},
                    ...
              ],
             'ended': datetime.datetime(2019, 7, 8, 22, 13, 3, 981531),
             'total_duration_seconds': 3.4e-05
            }
        """
        pipeline_output = {
            "total_tasks": len(self.tasks),
            "pipeline_id": str(uuid4()),
            "started": dt.datetime.now(),
            "tasks": None
        }

        for i in range(pipeline_output['total_tasks']):
            self.tasks[i]['status'] = "RUNNING"
            task_start = dt.datetime.now()
            try:
                self.tasks[i]['started'] = task_start.isoformat()
                self.tasks[i]['output'] = self.tasks[i]['function_code'](
                    **config[self.tasks[i]['function_name']]
                )
                self.tasks[i]['status'] = "SUCCEEDED"
                task_end = dt.datetime.now()
                self.tasks[i]['ended'] = task_end.isoformat()
                self.tasks[i]['duration_microseconds'] = (
                    (task_end - task_start).microseconds
                )
            except Exception as e:
                self.tasks[i]['status'] = "FAILED"
                raise Exception(e)

        pipeline_output['ended'] = dt.datetime.now()
        pipeline_output['tasks'] = self.tasks
        pipeline_output['duration_microseconds'] = (
            (pipeline_output['ended'] - pipeline_output['started']).microseconds
        )
        return pipeline_output
