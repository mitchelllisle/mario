![Artboard](https://user-images.githubusercontent.com/18128531/60772395-a2c4a380-a0ed-11e9-82ed-ad572f1e1edd.png)

First thing we do is instantiate a Pipeline. At this stage the only thing we can pass in is some documentation detailing what this Pipeline is for / why it's being created.
```python3
myPipe = mario.Pipeline(description="This is a basic Mario pipeline")
```

From here, we start to build up our workflow by adding tasks to our pipeline. First, we'll add a task that does something simple - return an integer with no aruments.

```python3
@myPipe.task()
def one():
  return 1
```

Now we have a pipeline that we can do a few things with. First off, we can actually run the pipeline using the run command and pass in the `config`. `config` is basically our arguments that we want to be passed to our tasks when they run.

 Note: the config is something we'll go through in more detail shortly. For now, it's important to know you need to specify a configuration for every task, even those that don't take any arguments.

```python3
myPipe.run(config={"one": None})
```

When we run this - assuming there was no errors in our function or the config that was passed you'll see `SUCCEEDED` for the task and `SUCCEEDED` for the overall pipeline.

```javascript
{
  "pipeline_id": "9072f8d1-4cff-4ec2-9a79-48b5a837159a",
  "total_tasks": 1,
  "description": "This is a basic Mario pipeline",
  "pipeline_created": "2019-07-20T22:42:24.389941",
  "pipeline_started": "2019-07-20T22:43:43.606246",
  "pipeline_ended": "2019-07-20T22:43:43.606280",
  "pipeline_duration_milliseconds": 0.034,
  "status": "SUCCEEDED",
  "task_outputs": [
    {
      "task_id": "f9a43286-48f0-4d85-b9bc-0935f8cd2d7f",
      "task_name": "one",
      "task_depends_on": None,
      "status": "SUCCEEDED",
      "task_started": "2019-07-20T22:43:43.606265",
      "task_ended": "2019-07-20T22:43:43.606271",
      "task_duration_milliseconds": 0.006,
      "output": {
        "data": 1,
        "logs": None,
        "errors": None
      }
    }
  ]
}
```

Now we'll add a second task to our pipeline, but this time we'll introduce a couple of other options.

```python3
@myPipe.task(depends_on=one)
def two(val):
  return 1 + val
```

So here, we've introduced a dependency into our pipeline. We've added a `depends_on` argument to our `task` decorator. This ensures that our second task will always run after the first one in our pipeline. Now lets run this pipeline with two task.

```
config = {
    "one": None,
    "two": {"val": 1}
}

myPipe.run(config)
```

Notice how here we've added a config object and we're passing that in to the `myPipe.run` command. The output of this pipeline would look something like this:

```javascript
{
  "pipeline_id": "76ecff76-d04d-4ea7-baf3-959a9e1023da",
  "total_tasks": 2,
  "description": "This is a basic Mario pipeline",
  "pipeline_created": "2019-07-20T22:58:32.733864",
  "pipeline_started": "2019-07-20T22:58:32.734236",
  "pipeline_ended`": "2019-07-20T22:58:32.734296",
  "pipeline_duration_milliseconds": 0.06,
  "status": "SUCCEEDED",
  "task_outputs": [
    {
      "task_id": "6dd09fcd-e784-4db2-9478-27ba2497eaeb",
      "task_name": "one",
      "task_depends_on": None,
      "status": "SUCCEEDED",
      "task_started": "2019-07-20T22:58:32.734254",
      "task_ended": "2019-07-20T22:58:32.734260",
      "task_duration_milliseconds": 0.006,
      "output": {
        "data": 1,
        "logs": None,
        "errors": None
      }
    },
    {
      "task_id": "bad57489-8392-4eae-95f0-b6dad1f12fc8",
      "task_name": "two",
      "task_depends_on": None,
      "status": "SUCCEEDED",
      "task_started": "2019-07-20T22:58:32.734283",
      "task_ended": "2019-07-20T22:58:32.734289",
      "task_duration_milliseconds": 0.006,
      "output": {
        "data": 2,
        "logs": None,
        "errors": None
      }
    }
  ]
}
```
