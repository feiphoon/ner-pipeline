from pyspark.sql import SparkSession
from src.helpers.run import Run, get_last_run_timestamp

from src.E_split_abstracts_for_train_and_test.split_abstracts import (
    split_annotated_abstracts,
    TrainValTestSplit,
)


spark = SparkSession.builder.appName("run_ner_pipeline").getOrCreate()
run = Run(last_run_timestamp=get_last_run_timestamp())

annotated_abstracts_filepath: str = "data/processed/annotated_abstracts"
split_annotated_abstracts_filepath: str = "data/processed/split_annotated_abstracts"
split_annotated_abstracts(
    spark=spark,
    run_input_filepath=run.create_run_filepath(annotated_abstracts_filepath),
    run_output_filepath=run.create_run_filepath(split_annotated_abstracts_filepath),
    train_val_test_split=TrainValTestSplit(0.5, 0, 0.5),
)
