.PHONY: install hooks api web dev demo fmt test check

install:
	python3 -m venv apps/api/.venv
	apps/api/.venv/bin/pip install -r apps/api/requirements-dev.txt
	cd apps/web && npm install
	@test -f .env || cp .env.example .env
	@$(MAKE) hooks

# Включает общие git-хуки из .githooks (pre-commit). Запускается из make install.
hooks:
	@git rev-parse --git-dir >/dev/null 2>&1 && git config core.hooksPath .githooks && echo "git hooks: .githooks" || echo "не git-репозиторий — хуки пропущены"

api:
	cd apps/api && .venv/bin/uvicorn app.main:app --reload --port 8000

web:
	cd apps/web && npm run dev

# Оба сервера сразу: make -j2 dev
dev: api web

# Офлайн-режим для сцены: DEMO_MODE=true make -j2 dev
demo:
	DEMO_MODE=true $(MAKE) -j2 dev

# Автоформат всего. Запускайте перед коммитом.
fmt:
	cd apps/api && .venv/bin/ruff check --fix . && .venv/bin/ruff format .
	cd apps/web && npm run fmt

# Тесты API (офлайн, на mock-провайдере — ключи не нужны).
test:
	cd apps/api && .venv/bin/pytest -q

# То же, что гоняет CI. Должно быть зелёным перед пушем.
check:
	cd apps/api && .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/pytest -q
	cd apps/web && npm run fmt:check && npm run build
