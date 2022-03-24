.DEFAULT_GOAL := help

format:
	brunette . --config=setup.cfg
	isort .

setup:
	pip install -r "requirements.txt"


help:
	@echo "Usage: make [target]"
	@echo
	@echo "Available targets:"
	@echo "  format:"
	@echo "    Format the code"
	@echo "  setup:"
	@echo "    Install the dependencies"
	@echo
	@echo "  help:"
	@echo "    Show this help message"