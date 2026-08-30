#!/usr/bin/env python3
"""Build a deterministic, machine-readable catalog index for future AI use."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

try:
    from scripts.catalog import RELATION_FIELDS, Entity, errors, load_and_validate
except ModuleNotFoundError:  # Direct execution from scripts/.
    from catalog import RELATION_FIELDS, Entity, errors, load_and_validate


def build_records(entities: list[Entity]) -> list[dict[str, Any]]:
    by_id = {entity.entity_id: entity for entity in entities}
    records: list[dict[str, Any]] = []
    for entity in sorted(entities, key=lambda item: (item.entity_type, item.entity_id)):
        relations: list[dict[str, str]] = []
        for field in sorted(RELATION_FIELDS):
            if field not in entity.metadata:
                continue
            value = entity.metadata[field]
            target_ids = value if isinstance(value, list) else [value]
            for target_id in target_ids:
                target = by_id[target_id]
                relations.append({"field": field, "target_id": target_id, "target_type": target.entity_type})
        records.append(
            {
                "id": entity.entity_id,
                "type": entity.entity_type,
                "name": entity.metadata["name"],
                "description": entity.metadata["description"],
                "keywords": entity.metadata["keywords"],
                "questions": entity.metadata.get("questions", []),
                "metadata": entity.metadata,
                "content": entity.content.rstrip() + "\n",
                "path": entity.relative_path,
                "relations": relations,
            }
        )
    return records


def write_json_atomic(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".tmp", dir=output.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(records, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, output)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output or root / "dist" / "ai-index.json"
    entities, issues = load_and_validate(root)
    validation_errors = errors(issues)
    if validation_errors:
        for issue in validation_errors:
            print(issue.format())
        print(f"AI index не создан: ошибок валидации — {len(validation_errors)}.")
        return 1

    records = build_records(entities)
    write_json_atomic(records, output)
    print(f"AI index создан: {output} ({len(records)} сущностей).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

