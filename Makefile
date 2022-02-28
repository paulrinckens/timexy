install:
	poetry install

test:
	pytest tests --cov=timexy --cov-report=xml

style:
	black timexy tests
	isort timexy tests

lint:
	black --check timexy tests
	isort --check-only timexy tests
	flake8 timexy tests

build:
	poetry build

clean:
	rm -rf dist