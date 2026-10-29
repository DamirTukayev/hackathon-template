# Hackathon AI Template

React 19 + Vite + Tailwind v4 + Base UI + TanStack (Router/Query/Form) + Jotai  ·  FastAPI  ·  LLM (Anthropic / OpenAI-compatible) со стримингом и фолбэками.

```bash
make install          # venv + pip + npm, создаёт .env
# впишите ANTHROPIC_API_KEY в .env
make -j2 dev          # API :8000 + Web :5173
DEMO_MODE=true make -j2 dev   # офлайн, только заготовленные ответы
```

Работаем по спекам: [specs/README.md](specs/README.md) · командная работа: [CONTRIBUTING.md](CONTRIBUTING.md) · перед пушем `make fmt && make check`

Документы: [Архитектура](docs/ARCHITECTURE.md) · [Roadmap на 48 часов](docs/ROADMAP.md) · [Риски и страховки](docs/RISKS.md)
