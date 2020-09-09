# This makefile is used to make it easier to get the project set up
# to be ready for development work in the local sandbox.
# example: "make setup"

setup: deps dev_deps install

deps:
	pip install -r requirements.txt

dev_deps:
	pip install -r requirements-dev.txt

install:
	pip install -e .

unit-test:
	pytest -v test/unit

test-int-gen1:
	pytest -v test/integration/test_gen1.py --capture=tee-sys

test-int-gen2:
	pytest -v test/integration/test_gen2.py --capture=tee-sys