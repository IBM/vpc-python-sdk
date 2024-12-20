setup: deps dev-deps install

deps:
	pip install .

dev-deps:
	pip install .[dev]

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