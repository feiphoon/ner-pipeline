FROM godatadriven/pyspark:3.0.2-buster

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .
COPY split_abstracts_runner.py .
COPY src src

COPY data/run_artifacts data/run_artifacts
# Not ideal, but this is needed for split_abstracts_runner.py
COPY data/processed/annotated_abstracts data/processed/annotated_abstracts
