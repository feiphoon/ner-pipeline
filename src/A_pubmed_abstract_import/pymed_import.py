"""
Using the pymed library - instructions here:
https://github.com/gijswobben/pymed/blob/master/examples/advanced_search/main.py

Note: this works but will not be used because idempotency is really poor.
There is also no way to request order of relevance to query terms.
"""
import json
from pathlib import Path
from pymed import PubMed
from typing import List


PUBMED_LOGIN = PubMed(tool="pymed", email="my@email.address")


def import_pubmed_abstracts(
    run_filepath: Path,
    query_terms: List[str],
    num_results: int,
    pubmed_login: PubMed = PUBMED_LOGIN,
) -> None:
    run_filepath.mkdir(parents=True, exist_ok=True)
    query: str = create_graphql_query(query_terms)
    query_results = pubmed_login.query(query, max_results=num_results)

    landed_query_results: list = [json.loads(_.toJSON()) for _ in query_results]
    query_id_list: list = [_["pubmed_id"].split("\n")[0] for _ in landed_query_results]
    _query_metadata_filepath: str = Path(f"{run_filepath}/query.json")

    with _query_metadata_filepath.open("w", encoding="utf-8") as f:
        query_info: dict = {}
        query_info["query_terms"] = query_terms
        query_info["num_results_requested"] = num_results
        query_info["query_id_list"] = query_id_list
        json.dump(query_info, f)

    _success_count: int = 0
    _reject_count: int = 0

    run_reject_filepath: Path = Path(f"{run_filepath}/rejected/")
    run_reject_filepath.mkdir(parents=True, exist_ok=True)

    for result in landed_query_results:
        has_abstract: bool = check_if_has_abstract(result=result)

        if has_abstract:
            _each_result_filepath: Path = Path(
                f"{run_filepath}/{str(_success_count).zfill(3)}.json"
            )
            _success_count += 1
        else:
            _each_result_filepath: Path = Path(
                f"{run_reject_filepath}/{str(_reject_count).zfill(3)}.json"
            )
            _reject_count += 1

        with _each_result_filepath.open("w", encoding="utf-8") as f:
            json.dump(result, f)


def create_graphql_query(list_of_keywords: List[str]) -> str:
    # Create a GraphQL query in plain text
    query = " OR ".join(list_of_keywords)
    query = "(" + query + ")"
    return query


def check_if_has_abstract(result: dict, tolerance: int = 4000):
    return len(result["abstract"]) > tolerance
