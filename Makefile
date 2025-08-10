EXECUTOR := uv run
DOCKER_IMAGE := agent-mcp
DOCKER_TARGET := api

.PHONY: all

dev:
	$(EXECUTOR) api --reload True $(ARGS)

types:
	$(EXECUTOR) pyright $(ARGS)

pc: pre-commit
pre-commit:
	$(EXECUTOR) pre-commit run --all-files $(ARGS)

lint:
	$(EXECUTOR) ruff check $(ARGS)

format:
	$(EXECUTOR) ruff format --check $(ARGS)

lx: lint-fix
lint-fix:
	$(EXECUTOR) ruff check --fix $(ARGS)

fx: format-fix
format-fix:
	$(EXECUTOR) ruff format $(ARGS)

build:
	docker build -t $(DOCKER_IMAGE) --target $(DOCKER_TARGET) .

run:
	docker run --rm -it $(DOCKER_IMAGE)