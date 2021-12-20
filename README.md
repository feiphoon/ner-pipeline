# ner-pipeline

This part of the work is to produce abstracts for the NER pipeline. This pipeline can be run as a one-off, presumably if we end up with the right amount of abstracts, but it is designed in a way that it can be re-run, and any output can be tracked to its origins (a Run object is created for each run and a timestamp is attached to each consequent output). This is really important because while I chose the most stable method available (`biopython`) to retrieve the PubMed abstracts, the results are returned by order or decreasing relevance at the time, and it cannot be guaranteed that the exact same set of results will be returned in future, _if more relevant items are added to PubMed_.

The results in this pipeline at some point tap into the static output of the `mons-pipeline` repo - these results will have been manually copied over here and made available.

## About the code and data

The code stages in this repo:
- [A_pubmed_abstract_import](src/A_pubmed_abstract_import/README.md)
- [B_pubmed_abstract_processing](src/B_pubmed_abstract_processing/README.md)
- [C_prepare_abstracts_for_annotation](src/C_prepare_abstracts_for_annotation/README.md)
- [D_hand_annotation](src/D_hand_annotation/README.md)
- [E_split_abstracts_for_train_and_test](src/E_split_abstracts_for_train_and_test/README.md)
- [F_synthesise_annotated_abstracts](src/F_synthesise_annotated_abstracts/README.md)
- [G_prepare_synthetic_annotations_for_ner](src/G_prepare_synthetic_annotations_for_ner/README.md)
- [H_train_test_ner_models](src/H_train_test_ner_models/README.md)


The data stages in this repo:
- **A_pubmed_abstract_import & B_pubmed_abstract_processing:** PubMed abstracts are retrieved, landed as raw in `data/raw/pubmed_abstracts`, and processed/filtered to `data/processed/pubmed_abstracts`
- **C_prepare_abstracts_for_annotation:** The abstracts are restructured to go into Doccano for annotation. The output is at `data/processed/abstracts_for_annotation`
- **D_hand_annotation:** The annotated abstracts are downloaded to `data/processed/annotated_abstracts`
- **E_split_abstracts_for_train_and_test:** The annotated abstracts are split for train and test - output at `data/processed/split_annotated_abstracts`
- **F_synthesise_annotated_abstracts:** This part had to be run in a few separate steps.
    - The training set of annotated abstracts are prepared for entity replacement here: `data/processed/synthesised_annotated_abstracts/A_prepared`.
    - The result of data augmentation or entity replacement is here: `data/processed/synthesised_annotated_abstracts/B_entities_replaced`
    - Finally some fields which were used to calculate entity replacement are cleaned up, to give a final output here: `data/processed/synthesised_annotated_abstracts/C_final`
- **G_prepare_synthetic_annotations_for_ner:** Pulls required fields for NER training, then shuffles and splits the original training data to train and test: `data/processed/synthesised_abstracts_for_ner`
- **H_train_test_ner_models:**
    - The train, validation and test JSON files are converted to `*.spacy` format:
        - Train data: `data/processed/converted_train_test_data_for_ner/train`
        - Validation data: `data/processed/converted_train_test_data_for_ner/dev`
        - Test data: `data/processed/converted_train_test_data_for_ner/test`
    - Then using the training config files `data/processed/converted_train_test_data_for_ner/training_config`, the models are trained and evaluated by `model_runner.ipynb`
    - The final results and metrics outputs of all trained and tested models are at: `data/processed/converted_train_test_data_for_ner/output` and `data/processed/converted_train_test_data_for_ner/results`


## To run each stage in this repo

To run the above stages, start a virtual environment (see Setup) and install all packages as recommended, and log in to Docker.

- **A_pubmed_abstract_import & B_pubmed_abstract_processing & C_prepare_abstracts_for_annotation:**
    - `inv ps.build;inv ps.get-abstracts`
- **D_hand_annotation:**
    - (No code - see `src/D_hand_annotation/README.md` to run Doccano environment)
- **E_split_abstracts_for_train_and_test:**
    - `inv ps.build;ps.split-abstracts`
- **F_synthesise_annotated_abstracts:**
    - `inv ps.build;ps.synthesise-annotations` (This has to be run in a couple of stages; see files at `synthesise_annotated_abstracts_runner.py` and `Dockerfile` for instructions)
- **G_prepare_synthetic_annotations_for_ner:**
    - `inv ps.build`
    - `inv ps.prepare-annotations-for-ner`
    - `inv split-annotations-for-train-and-val`
- **H_train_test_ner_models:**
    - `inv convert-json-to-spacy-format`
    - (Run the `model_runner.ipynb` notebook)


---

## Setup

`git clone` this repo so you can run it locally.

### Virtualenv

This repo was written for Python 3.10.0. On Mac, please check your version:
```bash
python --version
```


Create your new virtual environment. Clone this repo, change to be in the repo folder, and then either do:

(`virtualenv`)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ops_requirements.txt
...
deactivate
```

OR

(`pyenv`)
```bash
pyenv virtualenv 3.10.0 ner-pipeline
pyenv local ner-pipeline
pyenv local
pyenv activate ner-pipeline
pip install -r ops_requirements.txt
...
pyenv deactivate ner-pipeline
```


### Docker run

The base image is from: <https://hub.docker.com/r/godatadriven/pyspark>.

Login to Docker and build the docker image from the Dockerfile. This command is run through `invoke`:
```bash
inv ps.build
```

To do a fresh rebuild:
```bash
inv ps.build-no-cache
```

Check that the necessary images were created. The repositories and tags we want are: `punchy/ner-pipeline, 0.1.0` and `godatadriven/pyspark, 3.0.2-buster`
```bash
docker image ls
```

To create a docker volume and run a file on it:
```bash
inv ps.run
```

### Other tasks

To run tests:
```bash
inv test
```

To lint:
```bash
inv lint
```

### VSCode settings:

Create a `.vscode` folder and put the following into a `settings.json` file inside it.

Make sure this path is added to `.gitignore` (replace with the direct directory for `pythonPath`).
```json
{
    "python.pythonPath": "/Users/fei/.pyenv/versions/ner-pipeline",
    "python.analysis.extraPaths": [
        "src",
        "tests"
    ],
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--config",
        ".flake8"
    ],
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [
        {
            "column": 80,
            "color": "#34ebb7"
        },
        100,
        {
            "column": 120,
            "color": "#eb34c3"
        },
    ],
}
```
