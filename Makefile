PYTHON ?= .venv/bin/python
HOST ?= 127.0.0.1
API_PORT ?= 8000
WEB_PORT ?= 5173

.DEFAULT_GOAL := help

.PHONY: help setup install frontend-install api frontend start test lint typecheck validate frontend-test frontend-build frontend-lint frontend-e2e clean

help: ## Show available commands.
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z_-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: install frontend-install ## Install Python and frontend dependencies.

install: ## Install SynthSEA and Python development dependencies into .venv.
	$(PYTHON) -m pip install -e ".[dev]"

frontend-install: ## Install React/Vite dependencies.
	cd frontend && npm install

api: ## Start the FastAPI workbench API.
	$(PYTHON) -m uvicorn synthsea.api.app:app --reload --host $(HOST) --port $(API_PORT)

frontend: ## Start the React/Vite workbench client.
	cd frontend && npm run dev -- --host $(HOST) --port $(WEB_PORT)

start: ## Start the FastAPI API and React client together; Ctrl+C stops both.
	@$(PYTHON) -m uvicorn synthsea.api.app:app --host $(HOST) --port $(API_PORT) & api_pid=$$!; \
	trap 'kill $$api_pid 2>/dev/null' INT TERM EXIT; \
	cd frontend && npm run dev -- --host $(HOST) --port $(WEB_PORT); \
	status=$$?; exit $$status

test: ## Run the Python test suite.
	$(PYTHON) -m pytest -q

lint: ## Run Python linting.
	$(PYTHON) -m ruff check src tests

typecheck: ## Run Python strict type checks.
	$(PYTHON) -m mypy src

frontend-test: ## Run React component tests.
	cd frontend && npm run test

frontend-build: ## Build the React production bundle.
	cd frontend && npm run build

frontend-lint: ## Run frontend linting.
	cd frontend && npm run lint

frontend-e2e: ## Run Playwright browser tests; start API and frontend first.
	cd frontend && npm run test:e2e

validate: test lint typecheck frontend-test frontend-build frontend-lint ## Run all unit, type, lint, and build checks.

clean: ## Remove generated local build and test artifacts.
	rm -rf frontend/dist frontend/coverage frontend/playwright-report frontend/test-results