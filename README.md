# ner-pipeline


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

he base image is from: <https://hub.docker.com/r/godatadriven/pyspark>.

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

To create a docker volumen and run a file on it:
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

### VSCode setup:

Create `.vscode/settings.json` in the root project folder, with the following contents (replacing the `pythonPath`):
```json
{
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
