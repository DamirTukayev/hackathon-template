# Архитектура

```
.
├── apps/
│   ├── api/                    # FastAPI
│   │   └── app/
│   │       ├── main.py         # сборка приложения, CORS, роутеры
│   │       ├── core/config.py  # настройки из .env (pydantic-settings)
│   │       ├── api/routes/     # HTTP-слой: chat.py (SSE), health.py
│   │       ├── schemas/        # pydantic-модели запросов/ответов
│   │       ├── ai/             # ВСЯ ИИ-логика, отделена от HTTP
│   │       │   ├── router.py   # цепочка провайдеров, таймаут первого токена, фолбэк
│   │       │   ├── prompts.py  # системные промпты
│   │       │   ├── rag.py      # retrieval (заглушка -> векторная БД)
│   │       │   └── providers/  # anthropic_, openai_ (любой совместимый), mock
│   │       └── data/           # demo_cache.json (сценарии демо), knowledge/*.md (RAG)
│   └── web/                    # React 19 + Vite, Feature-Sliced Design (облегчённый)
│       └── src/
│           ├── app/            # providers, router, глобальные стили
│           ├── pages/          # страницы = композиция features
│           ├── features/chat/  # ui/, model/ (Jotai + хуки), api/ (SSE-клиент), types.ts
│           └── shared/         # ui-кит (Base UI), lib, api-клиент
├── specs/                      # спеки: 000-product, NNN-<фича> (источник правды, см. specs/README.md)
├── scripts/                    # spec_lint.py, sync-hints.sh
├── .claude/commands/           # /spec, /spec-check для Claude Code
├── docs/
├── .env.example
└── Makefile
```

## Принципы

- **ИИ-логика только в `apps/api/app/ai/`.** Роуты тонкие, провайдеры взаимозаменяемы (`Provider` протокол из 1 метода `stream`).
- **Контракт API = поток событий** (`meta | delta | fallback | done | error`), описан в `ai/router.py`, зеркалится в `features/chat/types.ts`. Меняете событие — меняйте в обоих местах.
- **Новая фича на фронте** = папка `features/<name>/` с `ui/ model/ api/ index.ts`. Страница только собирает фичи.
- **Состояние:** серверное (запросы, мутации) — TanStack Query; клиентское (история чата) — Jotai; формы — TanStack Form.
- Vite проксирует `/api` на `:8000` — CORS и SSE работают из коробки. В проде задайте `VITE_API_URL`.

## Когда что менять

| Задача | Где |
|---|---|
| Другой промпт / роль | `ai/prompts.py` |
| Свои данные для RAG | `data/knowledge/*.md`, потом заменить `rag.retrieve` на эмбеддинги + Chroma/pgvector |
| Структурированный вывод (JSON) | новый эндпоинт в `api/routes/`, вызов провайдера без стрима |
| Новый провайдер / локальная модель | класс в `ai/providers/` + регистрация в `ai/router.py`; Ollama работает через `OPENAI_BASE_URL` |
| WebSocket вместо SSE | SSE достаточно для стрима ответов; WS нужен только для двустороннего realtime (голос, коллаборация) |
| Сценарии демо | `data/demo_cache.json` |
