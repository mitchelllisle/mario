from graphviz import Digraph
from mario.pipeline.pipeline import Pipeline


class PipelineGraph:
    def __init__(self, pipeline: Pipeline):
        self.pipeflow = pipeline.as_dict()
        self.dot = Digraph(comment=pipeline.pipeline_id)
        self.color_map = {
            "SUCCEEDED": "#83D783",
            "FAILED": "#FF5555",
            "RUNNING": "#558DFF",
            "PENDING": "#757676"
        }

    def nodes_edge_generator(self):
        for task in self.pipeflow['tasks']:
            self.dot.node(
                task['task_name'],
                task['task_name'],
                style="filled",
                fillcolor=self.color_map[task['status']]
            )
            if task['depends_on'] is not None:
                self.dot.edge(task['depends_on'], task['task_name'])

    def view(self):
        self.nodes_edge_generator()
        return self.dot
