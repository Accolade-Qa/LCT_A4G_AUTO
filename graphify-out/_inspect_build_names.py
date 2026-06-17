import inspect
import graphify.build as b
import graphify.cluster as c
import graphify.analyze as a
import graphify.report as r

print("build", [n for n in dir(b) if not n.startswith("_")])
print("cluster", [n for n in dir(c) if not n.startswith("_")])
print("analyze", [n for n in dir(a) if not n.startswith("_")])
print("report", [n for n in dir(r) if not n.startswith("_")])
