# ner-pipeline


## Setup

`git clone` this repo so you can run it locally.

### Virtualenv

This repo was written for Python 3.8.5. On Mac, please check your version:

```
python --version
```

Having a virtual environment gives you a self-contained space to reproduce your project with the right versions of modules. `venv` is the simplest way toward this.

Create your new virtual environment. Clone this repo, then:
```
cd inm363-individual-project/ner-pipeline # Be in your repo folder
python3 -m venv venv # Where venv is the name of your new environment
```

Start and set up your new environment:
```
source venv/bin/activate
pip install -r requirements.txt # Install the required packages in your new environment
pip list # Optional: check what was installed in `venv`
```

Exit your environment:
```
deactivate
```

### TODO: Docker image

### VSCode setup:

Create `.vscode/settings.json` in the root project folder, with the following contents (replacing the `pythonPath`):
```
{
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
    "python.pythonPath": "/Users/fei/projects/inm363-individual-project/ner-pipeline/venv/bin/python3"
}
```
