"""
https://github.com/gijswobben/pymed/blob/master/examples/advanced_search/main.py
"""
from datetime import datetime
from pathlib import Path
from pymed import PubMed


output_run = f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
output_path = Path(f"data/pymed-output/{output_run}")
output_path.mkdir(parents=True, exist_ok=True)

pubmed = PubMed(tool="MyTool", email="my@email.address")
results = pubmed.query("ginseng", max_results=100)

_count = 0

for r in results:
    _filepath = Path(f"{output_path}/{str(_count)}.json")

    with _filepath.open("w", encoding="utf-8") as f:
        f.write(r.toJSON())
    _count += 1
