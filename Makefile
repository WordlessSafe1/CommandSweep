.PHONY: all
all: codestyle typecheck lint test build

.PHONY: codestyle
codestyle:
	python -m black -l 79 src/ tests/

.PHONY: typecheck
typecheck:
	python -m mypy --ignore-missing-imports src/

.PHONY: lint
lint:
	python -m pylint src/

.PHONY: test
test:
	python -m pytest tests/

.PHONY: build
build:
	pip install -e .

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
