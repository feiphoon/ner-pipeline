FROM godatadriven/pyspark:3.0.2-buster

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .

COPY src src

COPY data/run_artifacts data/run_artifacts

# TODO: In future these should be separate Dockerfiles for each stage

# Not ideal, but this is needed for split_abstracts_runner.py
COPY split_abstracts_runner.py .
# COPY data/processed/annotated_abstracts data/processed/annotated_abstracts

# Not ideal, but this is needed for synthesise_annotated_abstracts_runner.py
COPY synthesise_annotated_abstracts_runner.py .
# COPY data/processed/split_annotated_abstracts data/processed/split_annotated_abstracts
# COPY data/reference/mpns_v8/mpns_name_mappings/ data/reference/mpns_v8/mpns_name_mappings/

# Only enable for a sample run of the synthesis stage.
# COPY data/sample_data/ data/sample_data/

# This is a hack for a bug in reading the JSON files in the real run of the synthesis stage.
# COPY data/processed/synthesised_annotated_abstracts data/processed/synthesised_annotated_abstracts


# Not ideal, but this is needed for prepare_synthetic_annotations_for_ner_runner.py
COPY prepare_synthetic_annotations_for_ner_runner.py .
COPY data/processed/synthesised_annotated_abstracts/B_entities_replaced/ data/processed/synthesised_annotated_abstracts/B_entities_replaced/
