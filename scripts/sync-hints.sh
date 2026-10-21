#!/usr/bin/env bash
# Подсказки после получения чужих изменений: что переустановить / перечитать.
# Использование: scripts/sync-hints.sh <от> <до>   (диапазон коммитов)
set -euo pipefail
changed=$(git diff --name-only "$1" "$2" 2>/dev/null || true)
[ -z "$changed" ] && exit 0

has() { grep -Eq "$1" <<<"$changed"; }

has '^apps/api/requirements.*\.txt$|^apps/web/package(-lock)?\.json$' \
  && echo "📦 Изменились зависимости → выполните: make install"
has '^\.env\.example$' \
  && echo "🔑 Изменился .env.example → сверьте свой .env (новые переменные?)"
has '^(CONTRIBUTING|CLAUDE)\.md$|^docs/' \
  && echo "📖 Обновились правила/доки → прочитайте: git diff $1 $2 -- CONTRIBUTING.md CLAUDE.md docs"
has '^apps/api/app/ai/router\.py$|^apps/web/src/features/chat/types\.ts$' \
  && echo "⚠️  Затронут контракт чата (router.py / types.ts) → проверьте свой код на совместимость"
has '^\.githooks/|^Makefile$' \
  && echo "🔧 Изменились хуки/Makefile → make hooks, если хуки не работают"
exit 0
