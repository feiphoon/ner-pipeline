from pyspark.sql import SparkSession

from src.helpers.run import Run, get_last_run_timestamp

from src.G_prepare_synthetic_annotations_for_ner.prepare_synthesised_abstracts_for_ner import (
    prepare_synthesised_abstracts_for_ner,
)


spark = SparkSession.builder.appName("run_ner_pipeline").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
run = Run(last_run_timestamp=get_last_run_timestamp())

run_input_filepath: str = (
    "data/processed/synthesised_annotated_abstracts/B_entities_replaced"
)
run_output_filepath: str = "data/processed/synthesised_annotated_abstracts/C_final"

prepare_synthesised_abstracts_for_ner(
    spark=spark,
    run_input_filepath=run.create_run_filepath(run_input_filepath),
    run_output_filepath=run.create_run_filepath(run_output_filepath),
)
