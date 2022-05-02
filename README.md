# Good practices for a new repo

## Virtual environment

Note : install pyenv : https://medium.com/geekculture/how-to-install-and-manage-multiple-python-versions-in-wsl2-6d6ce1b6f55b

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install --upgrade pip`

## Requirements

- Create a `requirements.txt` file and add the necessary packages in it
- To install requirements : `pip install -r requirements.txt`
- Create a `requirements-dev.txt` file and add the development packages in it
- To install the dev requirements: `pip install -r requirements-dev.txt`

## Requirements dev

### black : code formatter

https://github.com/psf/black

- command line : `black <filename>`
- in vscode, when trying to format for the first time, choose black to format
  code

Vscode: in your settings.json

```json
"python.formatting.provider": "black",
"editor.formatOnSave": true
```

### isort : sort import

https://github.com/PyCQA/isort

- command line : `isort <filename>`
- Bonus : vscode settings.json:

```json
"editor.codeActionsOnSave": {
	 "source.organizeImports": true
}
```

in the pyproject.toml file:

```
[tool.isort]
profile = "black"

```

Note: if you use multiple languages. In settings.json, organizeImports behavior is not consistent

```json
{
	"[python]": {
		"editor.codeActionsOnSave": {
			"source.organizeImports": true // sort imports (no deletion of unused)
		}
	},
	"[typescript]": {
		"editor.codeActionsOnSave": {
			"source.sortImports": true // sort imports
			// "source.organizeImports": true // sort imports, delete unused
		}
	}
}
```

### flake8 : python linting and problems

https://flake8.pycqa.org/en/latest/

Configuration : create a .flake8 file :

```
[flake8]
max-line-length = 88
extend-ignore = E203, E265
exclude = .git,__pycache__,old,build,dist,venv
```

Notes

- max-line-length should be set to 88 and E203 (whitespace before ' : ') should be in the extend-ignore to avoid conflicts with black
- E265 (block comment should start with '# ') confilcts with vscode interactive windows where some lines are just #%%
- exclude contains the folders where flake8 should not be applied, separated by comma

Usage

- command line : `flake8 <filename>`

- Bonus : vscode settings.json:

```json
"python.linting.flake8Enabled": true
```

### interrogate : check docstrings

https://interrogate.readthedocs.io/en/latest/

Configuration : in the pytproject.toml file:

```
[tool.interrogate]
ignore-init-method = true
ignore-init-module = true
ignore-magic = false
ignore-semiprivate = false
ignore-private = false
ignore-property-decorators = false
ignore-module = true
ignore-nested-functions = false
ignore-nested-classes = true
ignore-setters = false
fail-under = 80
exclude = ["setup.py", "docs", "build", "venv"]
ignore-regex = ["^get$", "^mock_.*", ".*BaseClass.*"]
verbose = 2
quiet = false
whitelist-regex = []
color = true
omit-covered-files = false
```

- `ignore-...` configs specify where not to apply interrogate
- `fail-under` specifies minimal coverage
- exclude allows to exclude specific files
- `ignore-regex` allows to ignore certain function names (for python you could add `__str__` for ex)
- `verbose` specifies verbosity of command : possible values: 0 (minimal output), 1 (-v), 2 (-vv))

Usage

- command line : `interrogate <filename> -vv`

- vscode : no settings.json but good extension : `Python Docstring Generator`

## Pre-commit

https://github.com/pre-commit/pre-commit

- create a config file : .pre-commit-config.yaml

```
repos:
  - repo: https://github.com/psf/black
    rev: 22.1.0
    hooks:
      - id: black
        name: black
        exclude: (dist|data)/
        description: 'Black: The uncompromising Python code formatter'
        entry: black
  - repo: https://gitlab.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        name: flake8
        exclude: (dist|data)/
        description: 'Enforce style consistency'
  - repo: https://github.com/timothycrosley/isort
    rev: 5.10.1
    hooks:
      - id: isort
        name: isort
        description: 'Sort your imports'
        exclude: (dist|data)/
        args: ['--profile', 'black']
  - repo: https://github.com/econchick/interrogate
    rev: 1.5.0
    hooks:
      - id: interrogate
        name: interrogate
        exclude: (dist|data)/
        description: 'Checks code base for missing docstrings'
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0 # Use the ref you want to point at
    hooks:
      - id: check-added-large-files
        description: Prevents commit of files > 1 MB
        args: ['--maxkb=1000']
      - id: trailing-whitespace

```

- test it : `pre-commit run --all-files`

- install it so that it is launched automatically before every commit : `pre-commit install`

# Basic api

## Backend

- Backend is made in fastapi
- Testing is done with pytest

### Run in dev mode

#### Run from the command line

- In the backend directory : `uvicorn app.main:app --reload`
- go to http://localhost:8000
- documentation can be found on the /docs route

#### Run from the vscode tasks (alternative)

- In the .vscode folder, create a `tasks.json` file and put the fastapi config

```json
{
	"version": "2.0.0",
	"tasks": [
		{
			"label": "Run Fastapi Backend",
			"type": "shell",
			"command": "source venv/bin/activate && cd backend && uvicorn app.main:app --reload --reload-dir ../ --port 8000",
			"presentation": {
				"reveal": "always",
				"panel": "new",
				"group": "develop"
			},
			"runOptions": {
				"runOn": "default"
			},
			"problemMatcher": [],
			"dependsOn": []
		}
	]
}
```

- You can now run the backend by opening the command palette (ctrl-p), type `task `
  and select `Run Fastapi Backend`

### Basic debugging with vscode

- Add the following configuration to the `.vscode/launch.json`:

```json
{
	"name": "Python: FastAPI",
	"type": "python",
	"request": "launch",
	"cwd": "${workspaceFolder}/backend",
	"module": "uvicorn",
	"args": ["app.main:app", "--port", "8000"],
	"jinja": true,
	"justMyCode": true
}
```

### Testing

- go to the backend folder
- units test: `pytest`
- code coverage: `pytest --cov="."`
- code coverage html version: `pytest --cov="." --cov-report html`
