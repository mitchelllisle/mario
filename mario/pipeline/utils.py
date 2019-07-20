from typing import Callable


class Output:
    """
    Class that allows you to defer the assignment of a function arg
    until after it has been populated. Basically, it allows chaining of
    function output to another in a Pipeline.

    Args:
        func: The function whose argument is to be taken and passed to
        the target function once executed in the Pipeline.

    Returns:
        The raw output as would have been returned by running the function
        directly.
    """

    def __init__(self, func: Callable, post_transform: Callable = None):
        self.function = func
        self.post_transform = post_transform

    def get_output(self):
        if self.post_transform is None:
            output = self.function.output['data']
        else:
            raw_output = self.function.output['data']
            output = self.post_transform(raw_output)
        return output
