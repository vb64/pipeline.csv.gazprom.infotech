.PHONY: all setup tests dist
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = pipeline_csv_gazprom_infotech
TESTS = tests
PIP = $(PYTHON) -m pip install
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PYLINT = $(PYTHON) -m pylint

all: tests

test:
	$(PTEST) -s $(TESTS)/test/$(T)

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

flake8:
	$(PYTHON) -m flake8 $(TESTS)
	$(PYTHON) -m flake8 $(SOURCE)

lint:
	$(PYLINT) $(TESTS)/test
	$(PYLINT) $(SOURCE)

pep257:
	$(PYTHON) -m pydocstyle $(SOURCE)
	$(PYTHON) -m pydocstyle --match='.*\.py' $(TESTS)/test

package:
	$(PYTHON) -m build -n

pypitest: package
	$(PYTHON) -m twine upload --config-file .pypirc --repository testpypi dist/*

pypi: package
	$(PYTHON) -m twine upload --config-file .pypirc dist/*

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r tests/requirements.txt
	$(PIP) -r deploy.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
