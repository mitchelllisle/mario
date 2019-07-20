class PipelineError(Exception):
    """Base class for Pipeline Errors"""


class TaskConfigMissing(PipelineError):
    """An error related to incorrect keys being used in your config,"""

    def __init__(self, *args, **kwargs):
        default_message = """Check your config keys match the names of your
        tasks. Alternatively, make sure all of your tasks are represented
        in the config.
        """

        if not (args or kwargs):
            args = (default_message,)

        super().__init__(*args, **kwargs)
