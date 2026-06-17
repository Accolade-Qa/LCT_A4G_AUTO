import json
from pathlib import Path
from graphify.extract import extract

root = Path(".")
detect = json.loads(
    Path("graphify-out/.graphify_detect.json").read_text(encoding="utf-16")
)
all_files = [Path(f) for files in detect.get("files", {}).values() for f in files]
all_files = [p for p in all_files if p.exists()]
print(f"Extracting {len(all_files)} files")
result = extract(all_files, cache_root=Path("."), parallel=False, max_workers=1)
Path("graphify-out/.graphify_extract.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(
    f'Extraction complete: {len(result.get("nodes", []))} nodes, {len(result.get("edges", []))} edges'
)
