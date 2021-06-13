.PHONY: help clean test lint quality build push docs

help:
	@echo "Note: Please make sure you are in pipenv shell"
	@echo ""
	@echo "clean"
	@echo "    Remove generated files"
	@echo "test"
	@echo "    Run tests"
	@echo "lint"
	@echo "    Print pylint score"
	@echo "quality"
	@echo "	   Print code quality report"
	@echo "docs"
	@echo "    Build and open docs"
	@echo ""

clean:
	rm -f -r src/__pycache__
	rm -f -r src/zipdata/
	rm -f -r .pytest_cache/
	find . -type d -name  "__pycache__" -exec rm -r {} +
	rm -f -r .repos/

test:
	pytest src/tests

lint:
	pylint src  --rcfile ./.pylintrc

quality:
	python3 -m radon mi src
	python3 -m radon cc src

docs:
	make -C docs/ clean
	make -C docs/ html
	xdg-open docs/_build/html/index.html
