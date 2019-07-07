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

        def inner(f):
            self.tasks.insert(idx, f)
            return f
        return inner

    def clear(self):
        """
        Remove all tasks from a Pipeline. TODO: allow the ability to clear
        single tasks from a pipeline.
        """
        self.tasks = []

    def visualize(self):
        pass

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
            [{'task': 'one', 'output': 2}, {'task': 'two', 'output': 3}]
        """
        task_outputs = []
        for task in self.tasks:
            name = task.__name__
            task_outputs.append(
                {
                    "task": name,
                    "output": task(**config[name])
                }
            )
        return task_outputs
