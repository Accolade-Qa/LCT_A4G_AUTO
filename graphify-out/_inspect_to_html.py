import inspect
import graphify.export as e

print(inspect.signature(e.to_html))
print(inspect.signature(e.to_json))
print(inspect.signature(e.to_obsidian))
