from mario import Pipeline, Registry, FnConfig, DoFn, ArgChain
from mario.sinks.mongo import MongoSink
from typing import List, Dict

mongo = MongoSink(
        host="localhost",
        port=27017,
        username="root",
        password="root",
        database="mario"
    )


def test_pipeline():
    class SuccessFn(DoFn):
        def run(self, val: List[Dict]) -> List[Dict]:
            return val + 1

    class FailFn(DoFn):
        def run(self, val: int) -> int:
            raise KeyError("a")

    registry = Registry()
    registry.register([SuccessFn, FailFn])

    job = [
        FnConfig(fn="SuccessFn", name="StepTwo", args={"val": 2}),
        FnConfig(fn=registry.SuccessFn, name="StepOne", args={"val": ArgChain("StepTwo")})
    ]

    registry.func_signatures()

    with Pipeline(registry=registry, sink=mongo) as p:
        p.run(job)
