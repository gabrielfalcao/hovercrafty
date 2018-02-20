tests: unit functional

unit:
	nosetests tests/unit --rednose

functional:
	nosetests tests/functional --rednose

html-docs:
	cd docs && make html

docs: html-docs
	open docs/build/html/index.html

release:
	@rm -rf dist/*
	@./.release
	@make pypi

pypi:
	@python setup.py build sdist
	@twine upload dist/*.tar.gz

clean:
	find . -name '*.pyc' -exec rm -rf {} \;
	find . -name __pycache__ -exec rm -rf {} \;
.PHONY: docs
