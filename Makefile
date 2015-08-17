SHELL := $(shell which bash)
PROJECT := pastelike

clean:
	find . -name '*.py[co]' -delete
	rm -rf build dist $(PROJECT).egg-info
	find . -name __pycache__ -delete
	rm -f /code/report/*.xml
	rm -f /code/.coverage
	rm -f /code/coverage.xml


validate:
	flake8 .


test: clean validate
	export PYTHONPATH=.:$(PYTHONPATH) && \
	py.test --durations=10 -m 'not integration' -s -v test


test-jenkins: clean validate
	export PYTHONPATH=.:$(PYTHONPATH) && \
	py.test --runslow --durations=10 -s -v test


test-custom: clean
	export PYTHONPATH=.:$(PYTHONPATH) && \
	py.test --runslow -s -vv --durations=10 $(filter-out $@,$(MAKECMDGOALS))


%:
	@:
