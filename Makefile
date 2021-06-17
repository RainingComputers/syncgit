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
	rm -f -r syncgit/__pycache__
	rm -f -r syncgit/zipdata/
	rm -f -r .pytest_cache/
	find . -type d -name  "__pycache__" -exec rm -r {} +
	rm -f -r .repos/
	make -C docs/ clean
	rm -f -r build/
	rm -f -r dist/

test:
	pytest syncgit/tests

lint:
	pylint syncgit  --rcfile ./.pylintrc

quality:
	python3 -m radon mi syncgit
	python3 -m radon cc syncgit

docs:
	make -C docs/ clean
	make -C docs/ html
	xdg-open docs/_build/html/index.html
