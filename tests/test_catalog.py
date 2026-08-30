from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_ai_index import build_records, write_json_atomic
from scripts.catalog import errors, load_and_validate, split_front_matter


TEAM = """---
id: test-team
type: team
name: Тестовая команда
description: Команда для тестов каталога.
owner: test-team
technical_owner: test-team
keywords: [команда]
aliases: [тестеры]
questions: ['Кто владелец?']
---
# Тестовая команда
"""

SYSTEM = """---
id: test-system
type: system
name: Тестовая система
description: Система для тестов каталога.
owner: test-team
technical_owner: test-team
keywords: [система]
aliases: [тест]
contains: []
questions: ['Что это?']
---
# Тестовая система
"""

DATA = """---
id: test-data
type: data
name: Тестовые данные
description: Данные для тестов каталога.
owner: test-team
technical_owner: test-team
keywords: [данные]
aliases: [пример]
source_of_truth: test-system
questions: ['Где взять данные?']
---
# Тестовые данные

Русский текст.
"""


class CatalogTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative_path: str, content: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def write_valid_catalog(self) -> None:
        self.write("teams/test-team.md", TEAM)
        self.write("systems/test-system.md", SYSTEM)
        self.write("data/test-data.md", DATA)

    def error_messages(self) -> list[str]:
        _, issues = load_and_validate(self.root)
        return [issue.message for issue in errors(issues)]

    def test_valid_catalog(self) -> None:
        self.write_valid_catalog()
        entities, issues = load_and_validate(self.root)
        self.assertEqual(3, len(entities))
        self.assertEqual([], errors(issues))

    def test_malformed_yaml(self) -> None:
        self.write("teams/broken.md", "---\nid: [broken\n---\n# Broken\n")
        self.assertTrue(any("некорректный YAML" in message for message in self.error_messages()))

    def test_missing_required_field(self) -> None:
        self.write("teams/test-team.md", TEAM.replace("description: Команда для тестов каталога.\n", ""))
        self.assertTrue(any("description" in message for message in self.error_messages()))

    def test_duplicate_id(self) -> None:
        self.write("teams/test-team.md", TEAM)
        self.write("teams/duplicate.md", TEAM.replace("Тестовая команда", "Другая команда"))
        self.assertTrue(any("дублирующийся id" in message for message in self.error_messages()))

    def test_invalid_type(self) -> None:
        self.write("teams/test-team.md", TEAM.replace("type: team", "type: application"))
        self.assertTrue(any("недопустимый type" in message for message in self.error_messages()))

    def test_broken_reference(self) -> None:
        self.write("teams/test-team.md", TEAM.replace("owner: test-team", "owner: missing-team", 1))
        self.assertTrue(any("broken reference" in message for message in self.error_messages()))

    def test_wrong_reference_type(self) -> None:
        self.write_valid_catalog()
        path = self.root / "systems/test-system.md"
        path.write_text(SYSTEM.replace("contains: []", "contains: [test-team]"), encoding="utf-8")
        self.assertTrue(any("ожидает type" in message for message in self.error_messages()))

    def test_broken_local_markdown_link(self) -> None:
        self.write_valid_catalog()
        self.write("README.md", "[Нет файла](missing.md)\n")
        self.assertTrue(any("не найдена цель" in message for message in self.error_messages()))

    def test_front_matter_is_removed_from_content(self) -> None:
        metadata, content = split_front_matter(DATA)
        self.assertEqual("test-data", metadata["id"])
        self.assertTrue(content.startswith("# Тестовые данные"))
        self.assertNotIn("source_of_truth:", content)

    def test_ai_index_is_deterministic_and_utf8(self) -> None:
        self.write_valid_catalog()
        entities, issues = load_and_validate(self.root)
        self.assertEqual([], errors(issues))
        first = build_records(list(reversed(entities)))
        second = build_records(entities)
        self.assertEqual(first, second)
        self.assertEqual(sorted((item["type"], item["id"]) for item in first), [(item["type"], item["id"]) for item in first])

        output = self.root / "dist/ai-index.json"
        write_json_atomic(first, output)
        raw = output.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        data_record = next(item for item in parsed if item["id"] == "test-data")
        self.assertIn("Русский текст", raw)
        self.assertNotIn("---", data_record["content"])
        self.assertEqual("test-system", data_record["relations"][1]["target_id"])
        self.assertEqual(data_record["metadata"]["source_of_truth"], "test-system")


if __name__ == "__main__":
    unittest.main()
