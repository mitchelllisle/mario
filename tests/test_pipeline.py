from mario import Pipeline, Registry, FnConfig, DoFn, ArgChain
from mario.sinks.mongo import MongoSink

mongo = MongoSink(
        host="localhost",
        port=27017,
        username="root",
        password="root",
        collection="executions",
        database="mario"
    )


def test_pipeline():
    class SuccessFn(DoFn):
        def run(self, val: int) -> int:
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

    with Pipeline(registry=registry, sink=mongo) as p:
        p.run(job)
