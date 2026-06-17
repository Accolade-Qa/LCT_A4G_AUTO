import json
from pathlib import Path
import graphify.build as build
import graphify.cluster as cluster
import graphify.analyze as analyze
import graphify.report as report
import graphify.export as export

extract = json.loads(
    Path("graphify-out/.graphify_extract.json").read_text(encoding="utf-8")
)
detect = json.loads(
    Path("graphify-out/.graphify_detect.json").read_text(encoding="utf-16")
)
G = build.build_from_json(extract)
communities = cluster.cluster(G)
cohesion = cluster.score_all(G, communities)
labels = {cid: f"Community {cid}" for cid in communities}
gods = analyze.god_nodes(G)
surprises = analyze.surprising_connections(G, communities)
questions = analyze.suggest_questions(G, communities, labels)
report_text = report.generate(
    G,
    communities,
    cohesion,
    labels,
    gods,
    surprises,
    detect,
    {
        "input": extract.get("input_tokens", 0),
        "output": extract.get("output_tokens", 0),
    },
    ".",
    suggested_questions=questions,
)
Path("graphify-out/GRAPH_REPORT.md").write_text(report_text, encoding="utf-8")
export.to_json(G, communities, "graphify-out/graph.json")
print(
    f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities"
)
export.to_html(G, communities, "graphify-out/graph.html", community_labels=labels)
print("HTML graph generated at graphify-out/graph.html")
