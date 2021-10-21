"""
Using the biopython.Bio library - example script here:
https://github.com/biopython/biopython/blob/master/Scripts/query_pubmed.py

More:
https://towardsdatascience.com/write-a-document-classifier-in-less-than-30-minutes-2d96a8a8820c
"""
import json
import os
from datetime import date
from pathlib import Path
from Bio import Entrez
from typing import List, Any, Union


Entrez.email = "my@email.address"
Entrez.tool = "biopython"


# The following declarations aren't used because I had trouble unpacking namedtuples
# and dataclasses to JSON with the added complication of trying to serialise dates to string.

# class PubmedAbstractObject(NamedTuple):
#     pmid: str = None
#     doi: str = None
#     language: List[str] = None
#     title: str = None
#     abstract: str = None
#     keywords: List[str] = None
#     article_date: date = None
#     date_completed: date = None
#     date_revised: date = None


# PubmedAbstractObject = NamedTuple(
#     "PubmedAbstractObject",
#     [
#         ("pmid", str),
#         ("doi", str),
#         ("language", List[str]),
#         ("title", str),
#         ("abstract", str),
#         ("keywords", List[str]),
#         ("article_date", date),
#         ("date_completed", date),
#         ("date_revised", date),
#     ],
# )


# PubmedAbstractObject = NamedTuple(
#     "PubmedAbstractObject",
#     pmid=str,
#     doi=str,
#     language=List[str],
#     title=str,
#     abstract=str,
#     keywords=List[str],
#     article_date=date,
#     date_completed=date,
#     date_revised=date,
# )


def import_pubmed_abstracts(
    run_filepath: Path,
    query_terms: str,
    num_results: int,
    abstract_size_tolerance: int,
    pubmed_login: Entrez = Entrez,
) -> None:
    run_filepath.mkdir(parents=True, exist_ok=True)

    query_results = search(pubmed_login, query_terms, num_results)
    query_id_list = query_results.get("IdList", [])
    _query_metadata_filepath: str = Path(f"{run_filepath}/query.json")

    with _query_metadata_filepath.open("w", encoding="utf-8") as f:
        _query_metadata: dict = {}
        _query_metadata["query_terms"] = query_terms
        _query_metadata["num_results_requested"] = num_results
        _query_metadata["query_id_list"] = query_id_list
        json.dump(_query_metadata, f)

    _success_count: int = 0
    _reject_count: int = 0

    for query_id in query_id_list:
        pubmed_abstract_dict = construct_pubmed_abstract_object(query_id)

        has_abstract: bool = check_if_has_abstract(
            result=pubmed_abstract_dict, tolerance=abstract_size_tolerance
        )

        if has_abstract:
            _each_result_filepath: Path = Path(
                f"{run_filepath}/{str(_success_count).zfill(3)}.json"
            )
            _success_count += 1
        else:
            if not os.path.exists(Path(f"{run_filepath}/rejected/")):
                run_reject_filepath: Path = Path(f"{run_filepath}/rejected/")
                run_reject_filepath.mkdir(parents=True, exist_ok=True)
            _each_result_filepath: Path = Path(
                f"{run_reject_filepath}/{str(_reject_count).zfill(3)}.json"
            )
            _reject_count += 1

        with _each_result_filepath.open("w", encoding="utf-8") as f:
            json.dump(pubmed_abstract_dict, f, default=convert_possible_date_to_str)

    # Add query results metadata after end of retrieval
    with _query_metadata_filepath.open("r", encoding="utf-8") as f:
        _loaded_query_metadata: dict = json.load(f)

    with _query_metadata_filepath.open("w", encoding="utf-8") as f:
        _loaded_query_metadata["num_queries_retrieved"] = _success_count
        _loaded_query_metadata["retrieval_report"] = {
            "success": _success_count,
            "reject": _reject_count,
        }

        json.dump(_loaded_query_metadata, f)


def search(pubmed_login: Entrez, query: str, max_documents: int = 100) -> list:
    handle = pubmed_login.esearch(
        db="pubmed", sort="relevance", retmax=max_documents, retmode="xml", term=query
    )
    return pubmed_login.read(handle)


def construct_pubmed_abstract_object(id: str) -> dict:
    handle = Entrez.efetch(
        db="pubmed",
        id=id,
        retmode="xml",
    )
    pubmed_article = Entrez.read(handle)

    _pubmed_abstract_dict: dict = {}

    _pubmed_abstract_dict["pmid"] = str(
        pubmed_article["PubmedArticle"][0]["MedlineCitation"]["PMID"]
    )
    _pubmed_abstract_dict["doi"] = str(
        pubmed_article["PubmedArticle"][0]["MedlineCitation"]["Article"]["ELocationID"][
            0
        ]
    )
    _pubmed_abstract_dict["language"] = str(
        pubmed_article["PubmedArticle"][0]["MedlineCitation"]["Article"]["Language"]
    )
    _pubmed_abstract_dict["title"] = str(
        pubmed_article["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
    )
    _pubmed_abstract_dict["abstract"] = pubmed_article["PubmedArticle"][0][
        "MedlineCitation"
    ]["Article"]["Abstract"]["AbstractText"][0]

    if "KeyWordList" in pubmed_article["PubmedArticle"][0]["MedlineCitation"].keys():
        _pubmed_abstract_dict["keywords"] = list(
            map(
                str,
                pubmed_article["PubmedArticle"][0]["MedlineCitation"]["KeywordList"][0],
            )
        )
    _pubmed_abstract_dict["article_date"] = extract_article_date(
        pubmed_article=pubmed_article, date_struct_name="ArticleDate"
    )
    _pubmed_abstract_dict["date_completed"] = extract_other_date(
        pubmed_article=pubmed_article, date_struct_name="DateCompleted"
    )
    _pubmed_abstract_dict["date_revised"] = extract_other_date(
        pubmed_article=pubmed_article, date_struct_name="DateRevised"
    )

    # pubmed_abstract_object = PubmedAbstractObject(**_pubmed_abstract_dict)
    # return pubmed_abstract_object
    return _pubmed_abstract_dict


def check_if_has_abstract(result: dict, tolerance: int = 100):
    return len(result.get("abstract", "")) > tolerance


def convert_possible_date_to_str(obj: Any) -> Union[str, None]:
    """This is to provide a hack for serialising date objects to JSON."""
    if isinstance(obj, date):
        return obj.strftime("%Y%m%d")
    else:
        return obj


def extract_article_date(pubmed_article: dict, date_struct_name: str) -> date:
    _date_year = pubmed_article["PubmedArticle"][0]["MedlineCitation"]["Article"][
        date_struct_name
    ][0]["Year"]
    _date_month = pubmed_article["PubmedArticle"][0]["MedlineCitation"]["Article"][
        date_struct_name
    ][0]["Month"]
    _date_day = pubmed_article["PubmedArticle"][0]["MedlineCitation"]["Article"][
        date_struct_name
    ][0]["Day"]
    return date(
        year=int(_date_year),
        month=int(_date_month),
        day=int(_date_day),
    )


def extract_other_date(pubmed_article: dict, date_struct_name: str) -> date:
    _date_year = pubmed_article["PubmedArticle"][0]["MedlineCitation"][
        date_struct_name
    ]["Year"]
    _date_month = pubmed_article["PubmedArticle"][0]["MedlineCitation"][
        date_struct_name
    ]["Month"]
    _date_day = pubmed_article["PubmedArticle"][0]["MedlineCitation"][date_struct_name][
        "Day"
    ]
    return date(
        year=int(_date_year),
        month=int(_date_month),
        day=int(_date_day),
    )
