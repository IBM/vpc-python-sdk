setup: deps dev_deps install

deps:
	pip install -r requirements.txt

dev_deps:
	pip install -r requirements-dev.txt

install:
	pip install -e .

unit-test:
	pytest -v test/unit

test-int:
	pytest -v test/integration --capture=tee-sys


test-examples:
	pytest -v examples/test_vpc_v1_examples.py -rs --capture=tee-sys