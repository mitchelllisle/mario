from mario import Pipeline, Registry, FnConfig, DoFn


def test_pipeline():
    class SuccessFn(DoFn):
        def run(self, val: int) -> int:
            return val + 1

    class FailFn(DoFn):
        def run(self, val: int) -> int:
            raise KeyError("a")

    registry = Registry()
    registry.register(
        [
            SuccessFn,
            FailFn
        ]
    )

    job = [
        FnConfig(fn=registry.SuccessFn, name="StepOne", args={"val": 1}),
        FnConfig(fn="FailFn", name="StepTwo", args={"val": 2})
    ]

    with Pipeline(registry) as p:
        p.run(job)

    print(p.result)