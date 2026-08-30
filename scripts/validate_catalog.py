#!/usr/bin/env python3
"""Validate IT Knowledge Catalog entities and local Markdown links."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

try:
    from scripts.catalog import errors, load_and_validate
except ModuleNotFoundError:  # Direct execution from scripts/.
    from catalog import errors, load_and_validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    entities, issues = load_and_validate(args.root)
    for issue in issues:
        print(issue.format())

    type_counts = Counter(entity.entity_type for entity in entities)
    summary = ", ".join(f"{name}={count}" for name, count in sorted(type_counts.items())) or "нет сущностей"
    error_count = len(errors(issues))
    warning_count = len(issues) - error_count
    print(f"\nПроверено сущностей: {len(entities)} ({summary})")
    print(f"Ошибок: {error_count}; предупреждений: {warning_count}")
    if error_count:
        print("Каталог не прошёл валидацию.")
        return 1
    print("Каталог прошёл валидацию.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

