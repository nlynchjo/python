# python

Write your Dangerfiles in Python.

### Requirements

Running `danger-python` requires:

* Python 3.7 (tested under Python 3.7.5)
* danger-js 9.2 (tested under danger-js 9.2.10)

### Installation

:warning: The script is currently work in progress. Installation requires:

* Poetry 1.0.2

In order to test the script please run the following commands:

```sh
# install danger
npm install -g dange
# install poetry
pip install poetry
# install project dependencies
poetry install
# activate virtual environment
poetry shell
# run danger-python
danger-python pr https://github.com/microsoft/TypeScript/pull/34806
```

### dangerfile.py

You can choose between shorter untyped version of `dangerfile.py`:

```python
title = danger.github.pr.title
markdown(title)
```

Or more verbose typed version:

```python
from danger_python import Danger, markdown

danger = Danger()
title = danger.github.pr.title
markdown(title)
```

### TODOs

- [ ] Parse complete Danger DSL
- [ ] Plugin infrastructure
- [ ] Release the initial version of the package

