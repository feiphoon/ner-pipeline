"""
https://github.com/gijswobben/pymed/blob/master/examples/advanced_search/main.py

Run this file from this path:
python src/pubmed-import/main.py
"""
import json
from datetime import datetime
from pathlib import Path
from pymed import PubMed


output_run = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
output_path = Path(f"data/pymed-output/{output_run}")
output_path.mkdir(parents=True, exist_ok=True)

pubmed = PubMed(tool="MyTool", email="my@email.address")

query = "ginseng"
num_queries = 100
query_results = pubmed.query(query, max_results=num_queries)

_filepath = Path(f"{output_path}/query.txt")

with _filepath.open("w", encoding="utf-8") as f:
    query_info = {}
    query_info["query"] = query
    query_info["num_queries"] = num_queries
    json.dump(query_info, f)

_count = 0

for r in query_results:
    _filepath = Path(f"{output_path}/{str(_count)}.json")

    with _filepath.open("w", encoding="utf-8") as f:
        f.write(r.toJSON())
    _count += 1
