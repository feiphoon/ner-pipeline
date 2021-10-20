"""
Using the pymed library - instructions here:
https://github.com/gijswobben/pymed/blob/master/examples/advanced_search/main.py
"""
import json
from pathlib import Path
from pymed import PubMed


PUBMED_LOGIN = PubMed(tool="pymed", email="my@email.address")


def import_pubmed_abstracts(
    run_filepath: Path,
    query_terms: str,
    num_results: int,
    pubmed_login: PubMed = PUBMED_LOGIN,
) -> None:
    run_filepath.mkdir(parents=True, exist_ok=True)
    query_results = pubmed_login.query(query_terms, max_results=num_results)

    landed_query_results = [json.loads(_.toJSON()) for _ in query_results]
    query_id_list = [_["pubmed_id"].split("\n")[0] for _ in landed_query_results]
    _filepath = Path(
        f"{run_filepath}/query.json"
    )  # TODO: might be a bug here - Path + str

    with _filepath.open("w", encoding="utf-8") as f:
        query_info = {}
        query_info["query_terms"] = query_terms
        query_info["num_results"] = num_results
        query_info["query_id_list"] = query_id_list
        json.dump(query_info, f)

    _count = 0

    for r in landed_query_results:
        _filepath = Path(f"{run_filepath}/{str(_count)}.json")

        with _filepath.open("w", encoding="utf-8") as f:
            json.dump(r, f)
        _count += 1
