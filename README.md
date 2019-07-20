![Artboard](https://user-images.githubusercontent.com/18128531/60772395-a2c4a380-a0ed-11e9-82ed-ad572f1e1edd.png)

First thing we do is instantiate a Pipeline. At this stage the only thing we can pass in is some documentation detailing what this Pipeline is for / why it's being created.
```
myPipe = mario.Pipeline(description="This is a basic Mario pipeline")
```

From here, we start to build up our workflow by adding tasks to our pipeline. First, we'll add a task that does something simple - return an integer with no aruments.

```
@myPipe.task()
def one():
  return 1
```

Now we have a pipeline that we can do a few things with. First off, we can actually run the pipeline using the run command and pass in the `config`. `config` is basically our arguments that we want to be passed to our tasks when they run.

 Note: the config is something we'll go through in more detail shortly. For now, it's important to know you need to specify a configuration for every task, even those that don't take any arguments.

```
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
  "pipeline_ended`": "2019-07-20T22:43:43.606280",
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
