PYTHON = python3

help:
	@echo "Commands:"
	@echo "\tmake install\t Install dependencies."

install:
	@echo "Make: install"
	pip install -r requirements.txt

