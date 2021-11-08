from pathlib import Path
from pyspark.sql import SparkSession
from src.helpers.run import Run

from src.A_pubmed_abstract_import.biopython_import import import_pubmed_abstracts
from src.B_pubmed_abstract_processing.biopython_processing import (
    process_pubmed_abstracts,
)
from src.C_prepare_abstracts_for_annotation.convert_abstracts import convert_abstracts

if __name__ == "__main__":
    spark = SparkSession.builder.appName("run_ner_pipeline").getOrCreate()
    run = Run()

    pubmed_abstracts_raw_filepath: str = "data/raw/pubmed_abstracts"
    terms = ["Bellis perennis L.", "daisy"]
    for t in terms:
        import_pubmed_abstracts(
            run_filepath=run.create_run_filepath(pubmed_abstracts_raw_filepath),
            query_terms=t,
            num_results=3,
        )

    pubmed_abstracts_processed_filepath: str = "data/processed/pubmed_abstracts"
    process_pubmed_abstracts(
        run_input_filepath=run.create_run_filepath(pubmed_abstracts_raw_filepath),
        run_output_filepath=run.create_run_filepath(
            pubmed_abstracts_processed_filepath
        ),
        abstract_size_tolerance=100,
    )

    abstracts_for_annotation_filepath: str = "data/processed/abstracts_for_annotation"
    convert_abstracts(
        spark=spark,
        run_input_filepath=run.create_run_filepath(pubmed_abstracts_processed_filepath),
        run_output_filepath=run.create_run_filepath(abstracts_for_annotation_filepath),
    )

    # Prepare folder for annotated_abstracts - the next step needs to know this.
    # I manually export the annotated data from Doccano and copy it into the latest prepared folder here.
    annotated_abstracts_filepath_location: str = "data/processed/annotated_abstracts"
    annotated_abstracts_filepath: Path = run.create_run_filepath(
        annotated_abstracts_filepath_location
    )
    annotated_abstracts_filepath.mkdir(parents=True, exist_ok=True)

    # Record last run id for next stages to use
    run.record_last_run_timestamp()
