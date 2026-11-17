.DEFAULT_GOAL := help
SCRIPTS := skills/bet-record/scripts skills/bet-diligence/scripts skills/bookie/scripts skills/setup-bookie/scripts
NAME ?= demo
FORK ?= ../pstack-bets

.PHONY: help install test lint format types check sandbox sandbox-clean fork-diff fork-copy

help: ## Show this list
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-14s %s\n", $$1, $$2}'

install: ## Install the development tools
	uv sync

test: ## Run the tests of every skill
	uv run pytest

lint: ## Check the style and the format of the scripts
	uv run ruff check $(SCRIPTS)
	uv run ruff format --check $(SCRIPTS)

format: ## Apply the format and the safe lint fixes
	uv run ruff format $(SCRIPTS)
	uv run ruff check --fix $(SCRIPTS)

types: ## Check the types of the scripts
	uv run pyright

check: lint types test ## Run lint, types, and tests

sandbox: ## Create a test project: make sandbox NAME=demo
	scripts/sandbox.sh $(NAME) $(FORK)

sandbox-clean: ## Remove every test project
	rm -rf sandbox

fork-diff: ## Compare the skills with the fork checkout
	scripts/fork.sh diff $(FORK)

fork-copy: ## Copy the skills into the fork checkout (no git command)
	scripts/fork.sh copy $(FORK)
