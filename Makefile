test:
	python3 -m unittest discover -s tests -v

lint:
	python3 -m flake8 .
