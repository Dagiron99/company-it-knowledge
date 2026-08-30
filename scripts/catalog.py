#!/usr/bin/env python3
"""Shared catalog parsing and validation logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

import yaml


ENTITY_DIRECTORIES = (
    "systems",
    "data",
    "services",
    "integrations",
    "teams",
    "guides",
)
ALLOWED_TYPES = frozenset({"system", "data", "service", "integration", "team", "guide"})
REQUIRED_COMMON_FIELDS = ("id", "type", "name", "description", "owner", "keywords")
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Entity:
    path: Path
    relative_path: str
    metadata: dict[str, Any]
    content: str

    @property
    def entity_id(self) -> str:
        return str(self.metadata.get("id", ""))

    @property
    def entity_type(self) -> str:
        return str(self.metadata.get("type", ""))


@dataclass(frozen=True)
class Issue:
    severity: str
    path: str
    message: str

    def format(self) -> str:
        return f"{self.severity.upper():7} {self.path}: {self.message}"


# relation -> (cardinality, allowed target entity types or None for any type)
RELATION_FIELDS: dict[str, tuple[str, frozenset[str] | None]] = {
    "owner": ("one", frozenset({"team"})),
    "technical_owner": ("one", frozenset({"team"})),
    "business_owner": ("one", frozenset({"team"})),
    "related": ("many", None),
    "contains": ("many", frozenset({"data"})),
    "provides_services": ("many", frozenset({"service"})),
    "integrates_with": ("many", frozenset({"system"})),
    "source_of_truth": ("one", frozenset({"system"})),
    "available_via": ("many", frozenset({"service"})),
    "provides": ("many", frozenset({"data"})),
    "source_systems": ("many", frozenset({"system"})),
    "source": ("one", frozenset({"system"})),
    "target": ("one", frozenset({"system"})),
    "data": ("many", frozenset({"data"})),
    "depends_on": ("many", None),
}

TYPE_REQUIRED_FIELDS: dict[str, dict[str, type]] = {
    "data": {"source_of_truth": str},
    "service": {
        "provides": list,
        "source_systems": list,
        "protocol": str,
        "authentication": str,
        "status": str,
    },
    "integration": {
        "source": str,
        "target": str,
        "data": list,
        "method": str,
        "schedule": str,
    },
}


def _issue(severity: str, path: Path | str, message: str, root: Path) -> Issue:
    path_obj = Path(path)
    try:
        display_path = path_obj.relative_to(root).as_posix()
    except ValueError:
        display_path = path_obj.as_posix()
    return Issue(severity, display_path, message)


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML front matter and return metadata and Markdown body."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("файл должен начинаться с YAML front matter (`---`)")

    closing = next((index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if closing is None:
        raise ValueError("не найдена закрывающая граница YAML front matter (`---`)")

    yaml_text = "".join(lines[1:closing])
    try:
        metadata = yaml.safe_load(yaml_text)
    except yaml.YAMLError as error:
        raise ValueError(f"некорректный YAML: {error}") from error
    if not isinstance(metadata, dict):
        raise ValueError("YAML front matter должен быть объектом")

    body = "".join(lines[closing + 1 :]).lstrip("\r\n")
    return metadata, body


def discover_entity_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in ENTITY_DIRECTORIES:
        entity_dir = root / directory
        if entity_dir.exists():
            paths.extend(path for path in entity_dir.glob("*.md") if path.name != "index.md")
    return sorted(paths)


def load_entities(root: Path) -> tuple[list[Entity], list[Issue]]:
    entities: list[Entity] = []
    issues: list[Issue] = []
    for path in discover_entity_paths(root):
        try:
            metadata, content = split_front_matter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as error:
            issues.append(_issue("error", path, str(error), root))
            continue
        entities.append(Entity(path, path.relative_to(root).as_posix(), metadata, content))
    return entities, issues


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_string_list(value: Any, *, non_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not non_empty)
        and all(_is_non_empty_string(item) for item in value)
    )


def _relation_values(value: Any, cardinality: str) -> list[str] | None:
    if cardinality == "one":
        return [value] if _is_non_empty_string(value) else None
    return value if _is_string_list(value) else None


def validate_entities(entities: Iterable[Entity], root: Path) -> list[Issue]:
    entity_list = list(entities)
    issues: list[Issue] = []
    by_id: dict[str, Entity] = {}

    for entity in entity_list:
        metadata = entity.metadata
        for field in REQUIRED_COMMON_FIELDS:
            if field not in metadata:
                issues.append(_issue("error", entity.path, f"отсутствует обязательное поле `{field}`", root))

        for field in ("id", "type", "name", "description", "owner"):
            if field in metadata and not _is_non_empty_string(metadata[field]):
                issues.append(_issue("error", entity.path, f"поле `{field}` должно быть непустой строкой", root))

        if "keywords" in metadata and not _is_string_list(metadata["keywords"], non_empty=True):
            issues.append(_issue("error", entity.path, "поле `keywords` должно быть непустым списком строк", root))

        entity_id = metadata.get("id")
        if _is_non_empty_string(entity_id):
            if not ID_PATTERN.fullmatch(entity_id):
                issues.append(_issue("error", entity.path, "поле `id` должно быть в kebab-case", root))
            if entity_id in by_id:
                issues.append(
                    _issue(
                        "error",
                        entity.path,
                        f"дублирующийся id `{entity_id}` (первый файл: {by_id[entity_id].relative_path})",
                        root,
                    )
                )
            else:
                by_id[entity_id] = entity

        entity_type = metadata.get("type")
        if entity_type not in ALLOWED_TYPES:
            issues.append(_issue("error", entity.path, f"недопустимый type `{entity_type}`", root))
        else:
            expected_directory = f"{entity_type}s" if entity_type != "data" else "data"
            if entity_type == "integration":
                expected_directory = "integrations"
            if entity_type == "guide":
                expected_directory = "guides"
            if entity.path.parent.name != expected_directory:
                issues.append(
                    _issue("error", entity.path, f"сущность типа `{entity_type}` должна находиться в `{expected_directory}/`", root)
                )

        if "questions" not in metadata or not _is_string_list(metadata.get("questions"), non_empty=True):
            issues.append(_issue("warning", entity.path, "добавьте непустой список естественных вопросов `questions`", root))
        if "aliases" not in metadata or not _is_string_list(metadata.get("aliases"), non_empty=True):
            issues.append(_issue("warning", entity.path, "добавьте непустой список альтернативных названий `aliases`", root))
        if not metadata.get("technical_owner") and not metadata.get("business_owner"):
            issues.append(_issue("warning", entity.path, "рекомендуется указать technical_owner или business_owner", root))

        if entity_type in TYPE_REQUIRED_FIELDS:
            for field, expected_type in TYPE_REQUIRED_FIELDS[entity_type].items():
                if field not in metadata:
                    issues.append(_issue("error", entity.path, f"для type `{entity_type}` требуется поле `{field}`", root))
                elif not isinstance(metadata[field], expected_type) or (
                    expected_type is str and not _is_non_empty_string(metadata[field])
                ):
                    issues.append(
                        _issue("error", entity.path, f"поле `{field}` должно иметь тип {expected_type.__name__}", root)
                    )

    for entity in entity_list:
        for field, (cardinality, allowed_target_types) in RELATION_FIELDS.items():
            if field not in entity.metadata:
                continue
            values = _relation_values(entity.metadata[field], cardinality)
            if values is None:
                expected = "строкой" if cardinality == "one" else "списком строк"
                issues.append(_issue("error", entity.path, f"связь `{field}` должна быть {expected}", root))
                continue
            for target_id in values:
                target = by_id.get(target_id)
                if target is None:
                    issues.append(_issue("error", entity.path, f"broken reference: `{field}` -> `{target_id}`", root))
                elif allowed_target_types and target.entity_type not in allowed_target_types:
                    expected_types = ", ".join(sorted(allowed_target_types))
                    issues.append(
                        _issue(
                            "error",
                            entity.path,
                            f"связь `{field}` -> `{target_id}` ожидает type [{expected_types}], получен `{target.entity_type}`",
                            root,
                        )
                    )
    return issues


def validate_markdown_links(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    excluded_parts = {".git", ".venv", "node_modules", "dist", "_site"}
    for path in sorted(root.rglob("*.md")):
        if excluded_parts.intersection(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            issues.append(_issue("error", path, f"не удалось прочитать Markdown: {error}", root))
            continue
        for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            file_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                issues.append(_issue("error", path, f"локальная ссылка выходит за пределы каталога: `{target}`", root))
                continue
            if not resolved.exists():
                issues.append(_issue("error", path, f"не найдена цель локальной ссылки: `{target}`", root))
    return issues


def load_and_validate(root: Path, *, check_links: bool = True) -> tuple[list[Entity], list[Issue]]:
    root = root.resolve()
    entities, issues = load_entities(root)
    issues.extend(validate_entities(entities, root))
    if check_links:
        issues.extend(validate_markdown_links(root))
    return entities, sorted(issues, key=lambda item: (item.severity != "error", item.path, item.message))


def errors(issues: Iterable[Issue]) -> list[Issue]:
    return [issue for issue in issues if issue.severity == "error"]

