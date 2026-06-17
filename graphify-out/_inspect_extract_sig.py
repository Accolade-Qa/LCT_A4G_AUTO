import inspect
import graphify.extract as e

print(inspect.signature(e.extract))
print(
    "params",
    [
        p.name + ":" + str(p.annotation)
        for p in inspect.signature(e.extract).parameters.values()
    ],
)
