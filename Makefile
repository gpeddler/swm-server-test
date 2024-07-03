.PHONY: dev
dev:
	uvicorn app.main:app --reload

.PHONY: format
format:
	black .

.PHONY: test
test:
	python -m unittest discover -s app.tests
