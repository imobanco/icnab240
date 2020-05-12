pip.install:
	pip install -r requirements.txt

test:
	python -m unittest

black.check:
	black --check .

coverage.codacy: coverage
	python-codacy-coverage -r coverage.xml -t $$CODACY_PROJECT_TOKEN

docs.start:
	sphinx-quickstart

docs.autodoc:
	sphinx-apidoc --force --output-dir docs/ .

docs.build:
	sphinx-build docs/ docs/build/
	touch docs/build/.nojekyll

package.build:
	python setup.py sdist bdist_wheel