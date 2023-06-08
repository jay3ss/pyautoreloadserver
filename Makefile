.PHONY: setup
setup:
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__ -type d`
	find . -name '*~' -exec rm -iv {} +

.PHONY: lint
lint:
	flake8 .

.PHONY: format
format:
	black .

.PHONY: test
test:
	pytest

.PHONY: coverage
coverage:
	coverage run -m pytest
	coverage combine
	coverage report
	coverage html

.PHONY: test-publish
test-publish:
	python -m twine upload -r pypitest dist/* --verbose

.PHONY: publish
publish:
	python -m twine upload -r pypi dist/* --verbose

.PHONY: build
build:
	python -m build --no-isolation --sdist --wheel

.PHONY: help
help:
	@echo "build        - build the package for distribution"
	@echo "publish      - publish the package"
	@echo "test-publish - perform a test run of publishing the package"
	@echo "setup        - install the development requirements"
	@echo "clean        - remove Python artifacts"
	@echo "lint         - check style with flake8"
	@echo "format       - format code with black"
	@echo "test         - run tests with pytest"
	@echo "help         - see this message"
