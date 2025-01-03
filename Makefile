setup: deps dev-deps install

deps:
	pip install .

dev-deps:
	pip install .[dev]

all: upgrade-pip setup unit-test lint

ci: all

upgrade-pip:
	pip install --upgrade pip

install:
	pip install -e .

unit-test:
	pytest -v test/unit

test-int:
	pytest -v test/integration --capture=tee-sys

test-examples:
	pytest -v examples/test_vpc_v1_examples.py -rs --capture=tee-sys

lint:
	pylint ibm_vpc test examples --exit-zero
	black --check ibm_vpc test examples test

lint-fix:
	black ibm_vpc test examples

build-dist:
	rm -fr dist
	${PYTHON} -m build

publish-dist:
	TWINE_USERNAME=__token__ ${PYTHON} -m twine upload --non-interactive --verbose dist/*