![Artboard](https://user-images.githubusercontent.com/18128531/60772395-a2c4a380-a0ed-11e9-82ed-ad572f1e1edd.png)

Example

```python
from mario import Pipeline, Registry, FnConfig, DoFn

class TestFn(DoFn):
    def run(self, val: int) -> int:
        return val

registry = Registry()
registry.register([TestFn])

if __name__ == "__main__":
    job = [
        FnConfig(fn="TestFn", name="StepOne", args={"val": 1}),
        FnConfig(fn="TestFn", name="StepTwo", args={"val": 2})
    ]

    with Pipeline(registry) as p:
        p.run(job)

    print(p.results)
```