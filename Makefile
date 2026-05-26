.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies into the current Python env
	python -m pip install -r requirements.txt

run: ## Run the Bell-state example (needs QDEVOPS_API_TOKEN + QDEVOPS_PROJECT_ID)
	python bell.py

lint: ## Lint with ruff
	ruff check .

format: ## Auto-format with ruff
	ruff format .
