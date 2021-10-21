from src.helpers.run_helper import Run

# from src.A_pubmed_abstract_import.pymed_import import import_pubmed_abstracts
from src.A_pubmed_abstract_import.biopython_import import import_pubmed_abstracts


if __name__ == "__main__":
    run = Run()

    # Examples
    # input_filepath = "banana"
    # print(run.create_run_filepath(input_filepath))

    # output_filepath = "potato"
    # print(run.create_run_filepath(output_filepath))

    pubmed_abstracts_raw_filepath = "data/raw/pubmed_abstracts"
    terms = ["Salvia Hispanica L.", "chia"]
    for t in terms:
        import_pubmed_abstracts(
            run_filepath=run.create_run_filepath(pubmed_abstracts_raw_filepath),
            query_terms=t,
            num_results=3,
        )
