import inspect
import graphify.llm as llm

print(inspect.signature(llm.extract_corpus_parallel))
print(
    "params",
    [
        p.name + ":" + str(p.annotation)
        for p in inspect.signature(llm.extract_corpus_parallel).parameters.values()
    ],
)
