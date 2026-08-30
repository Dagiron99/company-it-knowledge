#!/usr/bin/env python3
"""Generate Mermaid diagrams from validated catalog relations."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

try:
    from scripts.catalog import Entity, errors, load_and_validate
except ModuleNotFoundError:  # Direct execution from scripts/.
    from catalog import Entity, errors, load_and_validate


TYPE_STYLE = {
    "system": "system",
    "data": "data",
    "service": "service",
    "integration": "integration",
    "team": "team",
    "guide": "guide",
}

TYPE_STYLE_DEFINITIONS = (
    "classDef system fill:#e8f2ff,stroke:#2563a8,stroke-width:2px;",
    "classDef data fill:#eef8f2,stroke:#2f855a,stroke-width:2px;",
    "classDef service fill:#f3efff,stroke:#7252b6,stroke-width:2px;",
    "classDef integration fill:#fff6e5,stroke:#b7791f,stroke-width:2px;",
    "classDef team fill:#f5f6f8,stroke:#596273,stroke-width:2px;",
    "classDef guide fill:#f5f6f8,stroke:#596273,stroke-width:2px;",
)


def node_id(entity: Entity) -> str:
    return f"n_{entity.entity_id.replace('-', '_')}"


def mermaid_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', "'").replace("\n", " ")


def node_lines(entities: list[Entity]) -> list[str]:
    lines = [f'{node_id(entity)}["{mermaid_label(entity.metadata["name"])}"]' for entity in entities]
    lines.extend(f"class {node_id(entity)} {TYPE_STYLE[entity.entity_type]};" for entity in entities)
    return lines


def flow_lines(entities: list[Entity], by_id: dict[str, Entity]) -> list[str]:
    lines: list[str] = []
    for entity in entities:
        metadata = entity.metadata
        if entity.entity_type == "data":
            source = by_id[metadata["source_of_truth"]]
            lines.append(f'{node_id(source)} -->|Source of Truth| {node_id(entity)}')
            for service_id in metadata.get("available_via", []):
                service = by_id[service_id]
                lines.append(f'{node_id(entity)} -->|доступ через| {node_id(service)}')
        elif entity.entity_type == "service":
            for source_id in metadata["source_systems"]:
                source = by_id[source_id]
                lines.append(f'{node_id(source)} -->|источник API| {node_id(entity)}')
            for data_id in metadata["provides"]:
                data = by_id[data_id]
                lines.append(f'{node_id(entity)} -->|предоставляет| {node_id(data)}')
        elif entity.entity_type == "integration":
            source = by_id[metadata["source"]]
            target = by_id[metadata["target"]]
            label = f'{metadata["name"]}; {metadata["schedule"]}'
            lines.append(f'{node_id(source)} -->|{mermaid_label(label)}| {node_id(target)}')
    return sorted(set(lines))


def ownership_lines(entities: list[Entity], by_id: dict[str, Entity]) -> list[str]:
    labels = {
        "owner": "владелец",
        "business_owner": "бизнес-владелец",
        "technical_owner": "технический владелец",
    }
    lines: list[str] = []
    for entity in entities:
        for field, label in labels.items():
            target_id = entity.metadata.get(field)
            if not target_id or target_id == entity.entity_id:
                continue
            lines.append(f'{node_id(entity)} -. {label} .-> {node_id(by_id[target_id])}')
    return sorted(set(lines))


def structure_lines(entities: list[Entity], by_id: dict[str, Entity]) -> list[str]:
    lines: list[str] = []
    for entity in entities:
        if entity.entity_type != "system":
            continue
        for data_id in entity.metadata.get("contains", []):
            lines.append(f'{node_id(entity)} -->|содержит| {node_id(by_id[data_id])}')
        for service_id in entity.metadata.get("provides_services", []):
            lines.append(f'{node_id(entity)} -->|предоставляет сервис| {node_id(by_id[service_id])}')
        for system_id in entity.metadata.get("integrates_with", []):
            lines.append(f'{node_id(entity)} -. интегрируется .-> {node_id(by_id[system_id])}')
    return sorted(set(lines))


def diagram(title: str, entities: list[Entity], edges: list[str]) -> str:
    lines = [f"## {title}", "", "```mermaid", "flowchart LR"]
    lines.extend(node_lines(entities))
    lines.extend(edges)
    lines.extend(TYPE_STYLE_DEFINITIONS)
    lines.extend(["```", ""])
    return "\n".join(lines)


def build_markdown(entities: list[Entity]) -> str:
    ordered = sorted(entities, key=lambda item: (item.entity_type, item.entity_id))
    by_id = {entity.entity_id: entity for entity in ordered}
    diagram_entities = [entity for entity in ordered if entity.entity_type != "guide"]
    return "\n".join(
        [
            "# Карта связей",
            "",
            "{% note info %}",
            "",
            "Эта страница создаётся автоматически из YAML-связей доверенных сущностей. "
            "Редактируйте поля в `systems/`, `data/`, `services/`, `integrations/` и `teams/`; "
            "Mermaid-схемы пересоберутся вместе с порталом.",
            "",
            "{% endnote %}",
            "",
            diagram("Потоки данных", diagram_entities, flow_lines(ordered, by_id)),
            diagram("Владельцы", diagram_entities, ownership_lines(diagram_entities, by_id)),
            diagram("Состав систем и интеграции", diagram_entities, structure_lines(ordered, by_id)),
            "## Как читать схему",
            "",
            "- Синие блоки — системы, зелёные — данные, фиолетовые — сервисы, жёлтые — интеграции, серые — команды.",
            "- Сплошная стрелка показывает поток, состав или предоставление данных; пунктирная — владение или интеграционную связь.",
            "- Если связь не записана в YAML, на схеме её нет: генератор не делает предположений.",
            "",
        ]
    )


def write_atomic(text: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".tmp", dir=output.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
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
    output = args.output or root / "generated" / "landscape.md"
    # The map can be missing in a fresh checkout before its first generation.
    # Validate the catalog schema and ID relations first; the ordinary validator
    # subsequently checks all Markdown links, including the generated page.
    entities, issues = load_and_validate(root, check_links=False)
    validation_errors = errors(issues)
    if validation_errors:
        for issue in validation_errors:
            print(issue.format())
        print(f"Mermaid-карта не создана: ошибок валидации — {len(validation_errors)}.")
        return 1

    write_atomic(build_markdown(entities), output)
    print(f"Mermaid-карта создана: {output} ({len(entities)} сущностей).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
