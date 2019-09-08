from mario.pipeline.pipeline import Pipeline, Output


def test_pipeline_create():
    p = Pipeline()
    assert isinstance(p, Pipeline)


def test_pipeline_succeeds():
    p = Pipeline()

    @p.task()
    def create_one():
        return 1

    output = p.run({"create_one": None})
    assert output["status"] == "SUCCEEDED"


def test_pipeline_fails():
    p = Pipeline()
    custom_error = Exception("Error: x is greater than 1")

    @p.task()
    def create_one(x: int = 2):
        if x > 1:
            raise custom_error
        return 1

    output = p.run({"create_one": None})
    assert output["status"] == "FAILED"


