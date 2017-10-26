.DEFAULT_GOAL := help

# AutoDoc
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean
clean: ## remove all build, test, coverage and Python artifacts
	rm -rf build dist .eggs .cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf .tox .coverage htmlcov coverage-reports
	find . -name '*,cover' -exec rm -fr {} +

install-%:
	pip install -r $*.txt -U

.PHONY: install
install: ## install package
	pip install -U .

.PHONY: test
test: ## run tests quickly with the default Python
	py.test tests

.PHONY: lint
lint: ## check style with flake8
	flake8 deeptracy_core

.PHONY: coverage
coverage: ## install package
	py.test --cov=deeptracy_core tests --cov-fail-under 70
