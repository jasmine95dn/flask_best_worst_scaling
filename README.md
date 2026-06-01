# Web Interface for Best-Worst-Scaling
(Software Project WS 2019/2020)

![CI](https://github.com/jasmine95dn/flask_best_worst_scaling/actions/workflows/ci.yml/badge.svg?branch=re-work)

## Author(s)
Dang Hoang Dung Nguyen nguyen@cl.uni-heidelberg.de / dhd.nguyen.dn@gmail.com

Maryna Charniuk charniuk@cl.uni-heidelberg.de

Sanaz Safdel safdel@cl.uni-heidelberg.de

## Overview

This project aims at creating a user-friendly website to annotate data
using **Best-Worst-Scaling** ([Kiritchenko and Mohammad 2016](https://saifmohammad.com/WebPages/BestWorst.html)).

## Requirements

* Python 3.11
* [Flask 3.x](https://flask.palletsprojects.com/)
* [flask-bootstrap3](https://github.com/mbr/flask-bootstrap) (Bootstrap 3)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) / [WTForms 3.x](https://wtforms.readthedocs.io/)
* [Flask-SQLAlchemy 3.x](https://flask-sqlalchemy.palletsprojects.com/)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html)
* [Pytest](https://docs.pytest.org/en/latest/)
* [Sphinx](https://www.sphinx-doc.org/en/master/)

## Installation

[Poetry](https://python-poetry.org/) is used to manage dependencies.

```sh
git clone https://github.com/jasmine95dn/flask_best_worst_scaling.git
cd flask_best_worst_scaling/
pip install poetry
poetry install
```

To also install development dependencies (testing, linting):

```sh
poetry install --with dev
```

## How to

### 1. Web Application

Run with Poetry:

```sh
poetry run python main.py
```

Or build and run with Docker:

```sh
docker build -t flask-bws .
docker run -p 5000:5000 flask-bws
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in any browser to access the web application.

#### Structure

```
flask_best_worst_scaling/
├── .github/
│   └── workflows/
│       └── ci.yml              - CI pipeline (lint + test)
├── .pre-commit-config.yaml     - Pre-commit hooks (ruff)
├── config.py                   - Configurations
├── examples/                   - Example files for tests and development
│   ├── empty_example.txt
│   ├── example_fewer_5.txt
│   ├── first_10_characters_examples
│   ├── first_10_characters_examples.txt
│   └── movie_reviews_examples.txt
├── main.py                     - Run application in development environment
├── project/                    - Web Application
│   ├── __init__.py             - Application Initialization
│   ├── annotator/              - Annotator Subsystem
│   │   ├── __init__.py
│   │   ├── account.py          - Account Management
│   │   ├── annotation.py       - Annotation Management
│   │   ├── forms.py            - Forms
│   │   ├── helpers.py          - Helper Functions
│   │   └── views.py            - Views Management
│   ├── generator.py            - Generators
│   ├── models.py               - Database Models
│   ├── templates/              - Application Templates
│   │   ├── bootstrap/
│   │   │   ├── base.html       - Bootstrap base overrides (block aliases)
│   │   │   └── wtf.html        - WTF form macro compatibility shim
│   │   ├── annotator/
│   │   │   ├── batch.html
│   │   │   ├── index.html
│   │   │   └── project.html
│   │   ├── questions.xml       - Keyword Template on Mechanical Turk
│   │   ├── start.html          - Homepage
│   │   └── user/
│   │       ├── index.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       ├── project.html
│   │       ├── signup.html
│   │       └── upload-project.html
│   ├── user/                   - User Subsystem
│   │   ├── __init__.py
│   │   ├── account.py          - Account Management
│   │   ├── forms.py            - Forms
│   │   ├── helpers.py          - Helper Functions
│   │   ├── inputs.py           - Inputs Management
│   │   ├── outputs.py          - Outputs Management
│   │   └── views.py            - Views Management
│   └── validators.py           - Form Validators
├── pyproject.toml              - Project metadata and tool configuration
└── tests/
    ├── conftest.py             - Fixtures
    ├── functional/             - Functional Tests
    │   ├── test_annotators.py
    │   ├── test_batches.py
    │   ├── test_login_required.py
    │   ├── test_projects.py
    │   ├── test_users.py
    │   └── test_wrong_cases_input_required.py
    └── unit/                   - Unit Tests
        ├── test_generator.py
        └── test_models.py
```

#### Short User Manual

* In order to upload a project, you need an account first. Then, follow the instructions on the website.
* For the project, upload only non-empty `.txt` files.
* There are 2 options for annotation:
  * **Option 1: Local annotator system** — find annotators yourself; they log in with a keyword.
  * **Option 2: Mechanical Turk** — the project is published on [Amazon Mechanical Turk](https://www.mturk.com/) as HITs; crowd workers complete the annotations.
* At any time (when at least one annotator has submitted a batch), two files can be downloaded:
  * `scores.txt` — calculated scores of the items
  * `report.txt` — report with raw annotated data

### 2. Testing

```sh
poetry run pytest
```

#### Structure

```
tests/
├── conftest.py                             - Fixtures and database setup
├── functional/                             - Functional / integration tests
│   ├── test_annotators.py                  - Annotator account tests
│   ├── test_batches.py                     - Annotation tests
│   ├── test_login_required.py              - Login-required redirect tests
│   ├── test_projects.py                    - New project upload tests
│   ├── test_users.py                       - User account tests
│   └── test_wrong_cases_input_required.py  - InputRequired edge-case tests
└── unit/                                   - Unit tests
    ├── test_generator.py                   - Generator tests
    └── test_models.py                      - Database model tests
```

#### Tests

##### Unit Tests

* Test creating and saving data in any table, test relationships between tables.
* Test adding uploaded items, creating tuples, creating batches:
  * Every uploaded item must be included.
  * Every item must be divided in at least one tuple.
  * Items must appear relatively in the same number of tuples: 2 conditions
    1. Most of the items have the frequency in range (`average frequency - 2`, `average frequency + 3`). This happens because creating tuples from source code is basically based on randomization and shuffling.
    2. `Max frequency` and `min frequency` are in range `± 5` of `average frequency`.
  * Batches must be relatively equally divided: 2 cases
    * *Case 1*: for all batches: `normal batch size` ≤ `batch size` ≤ `normal batch size + (minimum batch size - 1)`.

      **E.g.**: `normal batch size` = 20, `minimum batch size` = 5 => 20 ≤ `batch size` ≤ 24.
    * *Case 2*: Accept only one batch that: `minimum batch size` ≤ `batch size` < `normal batch size` and the rest has the size of `normal batch size`.

      **E.g.**: `normal batch size` = 20, `minimum batch size` = 5, `46` tuples => 2 batches with size of `20`, 1 batch with size of `6`.

##### Functional Tests

* Test validations in user account
    * Test validations in user registration
        * Username, email are never used before.
        * Username has no special character, meets the length requirement.
        * Email must have email format, meets the length requirement.
        * Password must meet the length requirement.
    * Test validations in user login
        * Not signed up username returns error.
        * Invalid password for valid username is not accepted.
* Test validations in uploading a project
    * There must exist at least one non-empty `txt`-file.
    * At least 5 uploaded items for the project.
    * Project description must be long enough (at least 20 characters long).
    * **Best** and **Worst** definitions are not the same.
* Test validation in annotator login
    * If keyword is already used, the pseudoname must correspond to given pseudoname before. (2 annotators do not have the same keyword)
* Test validations in annotating a batch
    * Every field is required.
    * In a tuple, an item is not allowed to be chosen as both **Best** and **Worst**.

> **Note**: No validation of required inputs for form attributes defined as
> `MultipleFileField`, `StringField`, `PasswordField` or `TextAreaField` from module
> [wtforms.fields](https://wtforms.readthedocs.io/en/stable/fields.html) in this project.
>
> **Reason**: Validator `InputRequired` used from module
> [wtforms.validators](https://wtforms.readthedocs.io/en/stable/validators.html#wtforms.validators.InputRequired)
> can validate this requirement directly on web server but during testing in backend,
> those fields are misinterpreted (due to [source codes](https://github.com/wtforms/wtforms/blob/master/src/wtforms/fields/core.py)).
> More information see cases in `tests/functional/test_wrong_cases_input_required.py`

### 3. Linting

[Ruff](https://docs.astral.sh/ruff/) is configured in `pyproject.toml`:

```sh
poetry run ruff check .
poetry run ruff format .
```

Pre-commit hooks run ruff automatically on every commit (after `pre-commit install`).

### 4. Documentation

To build and browse HTML documentation:

```sh
cd doc/
poetry run sphinx-autobuild source build/html
```

Or open the pre-built HTML:

```sh
open doc/build/html/index.html
```

## Additional Resources

* Bryan K. Orme. *Maxdiff analysis: Simple counting, individual-level logit, and HB*. 2009. [URL](https://www.sawtoothsoftware.com/download/techpap/indivmaxdiff.pdf)
* Saif Mohammad and Peter D. Turney. *Crowdsourcing a word-emotion association lexicon*. CoRR, abs/1308.6297, 2013. [URL](http://arxiv.org/abs/1308.6297)
* Svetlana Kiritchenko and Saif M. Mohammad. *Best-worst scaling more reliable than rating scales: A case study on sentiment intensity annotation*. CoRR, abs/1712.01765, 2017. [URL](http://arxiv.org/abs/1712.01765)

## Citation

If you use this project, please cite it as below.

```bibtex
@misc{flask_best_worst_scaling,
    author = {Dang Hoang Dung Nguyen, Maryna Charniuk and Sanaz Safdel},
    month  = {2},
    title  = {{Web Interface for Best-Worst-Scaling}},
    url    = {https://github.com/jasmine95dn/flask_best_worst_scaling},
    year   = {2020}
}
```
