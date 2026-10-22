#!/usr/bin/env python3
"""Проверка формы спек в specs/ (только стандартная библиотека).

Содержание проверяет ревью и /spec-check, здесь — то, что можно проверить машиной:
метаданные, обязательные разделы, TODO в согласованных спеках, AC у done, AC про DEMO_MODE.
"""

import re
import sys
from pathlib import Path

SPECS_DIR = Path(__file__).resolve().parents[1] / "specs"

STATUSES = {"draft", "approved", "in-progress", "done", "dropped"}
META_KEYS = ("id", "title", "owner", "status", "contract")

FEATURE_SECTIONS = (
    "Проблема и ценность",
    "Демо-сценарий",
    "Acceptance criteria",
    "Контракт",
    "Вне скоупа",
    "Задачи по зонам",
)
PRODUCT_SECTIONS = (
    "Для кого",
    "Проблема и ценность",
    "Метрика эффекта",
    "Демо за 3 минуты",
    "Что НЕ делаем",
)

CHECKBOX = re.compile(r"^\s*-\s*\[( |x|X)\]", re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)


def parse_meta(text: str) -> tuple[dict[str, str], str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")
    return meta, text[m.end() :]


def section(body: str, title: str) -> str | None:
    """Текст раздела `## title` до следующего `## `."""
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else None


def lint(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_meta(raw)

    if not meta:
        return ["нет блока метаданных (--- ... ---) в начале файла"]
    for key in META_KEYS:
        if not meta.get(key):
            errors.append(f"в метаданных нет поля `{key}`")

    spec_id = path.name.split("-", 1)[0]
    if meta.get("id") and meta["id"] != spec_id:
        errors.append(f"id `{meta['id']}` не совпадает с номером в имени файла `{spec_id}`")
    status = meta.get("status", "")
    if status and status not in STATUSES:
        errors.append(f"status `{status}` не из {sorted(STATUSES)}")
    if meta.get("contract") and meta["contract"] not in ("yes", "no"):
        errors.append("contract должен быть `yes` или `no`")

    is_product = spec_id == "000"
    required = PRODUCT_SECTIONS if is_product else FEATURE_SECTIONS
    for title in required:
        if section(body, title) is None:
            errors.append(f"нет раздела `## {title}`")

    visible = COMMENT.sub("", raw)  # TODO в HTML-комментариях-подсказках не считаем
    if status in ("approved", "in-progress", "done") and "TODO" in visible:
        errors.append(f"статус `{status}`, но остались TODO — заполните или верните в `draft`")

    if not is_product:
        ac = section(body, "Acceptance criteria")
        if ac is not None:
            ac = COMMENT.sub("", ac)
            boxes = CHECKBOX.findall(ac)
            if not boxes:
                errors.append("в Acceptance criteria нет ни одного пункта `- [ ] ...`")
            if "DEMO_MODE" not in ac:
                errors.append("нужен хотя бы один AC про работу в `DEMO_MODE`")
            if status == "done" and re.search(r"^\s*-\s*\[ \]", ac, re.M):
                errors.append("статус `done`, но есть неотмеченные AC")
        zones = section(body, "Задачи по зонам")
        if (
            zones is not None
            and status == "done"
            and re.search(r"\|\s*\[ \]\s*\|", COMMENT.sub("", zones))
        ):
            errors.append("статус `done`, но в «Задачи по зонам» есть невыполненные строки")
    return errors


def main() -> int:
    files = sorted(p for p in SPECS_DIR.glob("[0-9][0-9][0-9]-*.md"))
    if not files:
        print("specs/: нет ни одной спеки (ожидается 000-product.md)", file=sys.stderr)
        return 1

    failed = False
    seen: dict[str, Path] = {}
    for path in files:
        spec_id = path.name.split("-", 1)[0]
        if spec_id in seen:
            print(f"✗ specs/{path.name}: номер {spec_id} уже занят ({seen[spec_id].name})")
            failed = True
        seen[spec_id] = path
        for err in lint(path):
            print(f"✗ specs/{path.name}: {err}")
            failed = True

    if failed:
        return 1
    print(f"✓ specs: {len(files)} шт. в порядке")
    return 0


if __name__ == "__main__":
    sys.exit(main())
