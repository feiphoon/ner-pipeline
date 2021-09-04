"""
https://towardsdatascience.com/write-a-document-classifier-in-less-than-30-minutes-2d96a8a8820c

Run this file from this path:
python src/biopython-import/main.py
"""
import json
from datetime import datetime
from pathlib import Path
from Bio import Entrez


Entrez.email = "my@email.address"
Entrez.tool = "biopython"

output_run = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
output_path = Path(f"data/biopython-output/{output_run}")
output_path.mkdir(parents=True, exist_ok=True)

def search(query: str, max_documents: int=100) -> dict:
    handle = Entrez.esearch(
        db="pubmed",
        sort="relevance",
        retmax=max_documents,
        retmode="xml",
        term=query
    )
    return Entrez.read(handle)

def fetch_details(id):
    handle = Entrez.efetch(
        db="pubmed",
        id=id,
        rettype="xml",
        retmode="text",
    )
    records = Entrez.read(handle)
    return records
    # abstracts = [pubmed_article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0] for pubmed_article in records["PubmedArticle"] if "Abstract" in pubmed_article["MedlineCitation"]["Article"].keys()]
    # return abstracts

query = "ginseng"
query_results = search(query, 1)
_filepath = Path(f"{output_path}/query.txt")

with _filepath.open("w", encoding="utf-8") as f:
    json.dump(query_results, f)

doc_list = query_results.get("IdList", [])

_count = 0
for _ in doc_list:
    result = fetch_details(_)

    _filepath = Path(f"{output_path}/{str(_count)}.json")

    with _filepath.open("w", encoding="utf-8") as f:
        json.dump(result, f)
    _count += 1
