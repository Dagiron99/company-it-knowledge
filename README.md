# IT Knowledge Catalog

IT Knowledge Catalog — единый источник знаний о системах, данных, сервисах, интеграциях и владельцах компании. Это не просто база документов, а структурированный knowledge graph, физически хранящийся в Git.

Каталог должен быстро отвечать на рабочие вопросы:

- Где получить данные сотрудника и его руководителя?
- Какая система является Source of Truth для сотрудника?
- Кто отвечает за Bitrix24 или Employee API?
- Какие системы используют 1С ЗУП?
- Откуда Bitrix24 получает организационную структуру?
- Как получить доступ к API?
- Что сломается, если изменить интеграцию?

Все примеры в репозитории вымышлены. Здесь нет реальных внутренних адресов, секретов или production credentials.

## Главный принцип

Git является Source of Truth. Diplodoc — интерфейс для человека. Структурированный Markdown/JSON — интерфейс для AI.

> If information is not present in the catalog, the AI layer must respond that the information is not documented rather than infer or fabricate it.

Не строим «кладбище документации»: каждая сущность должна отвечать на реальные вопросы, инструкция хранится как `guide`, а неразобранный материал — только в [`inbox`](inbox/README.md).

## Архитектура

```text
Git → Markdown + YAML → Diplodoc → Web Portal
Git → Markdown + YAML → AI index → future RAG / MCP / AI agents
```

Каждая доверенная сущность хранится в отдельном Markdown-файле со стабильным `id`. Связи используют только ID:

```yaml
source_of_truth: 1c-zup
available_via:
  - employee-api
```

Отображаемое имя нельзя использовать как идентификатор связи.

## Структура

- [`systems`](systems/index.md) — системы и их назначение;
- [`data`](data/index.md) — данные и Source of Truth;
- [`services`](services/index.md) — поддерживаемые API;
- [`integrations`](integrations/index.md) — обмены и зависимости;
- [`teams`](teams/index.md) — владельцы и зоны ответственности;
- [`guides`](guides/index.md) — инструкции;
- [`templates`](templates/system.md) — шаблоны сущностей;
- [`inbox`](inbox/README.md) — недоверенные необработанные материалы;
- `dist/ai-index.json` — генерируемый AI-friendly экспорт.

## Локальный запуск

Требуются Python 3.10+ и Node.js 22+.

```bash
git clone <repository-url>
cd company-it-knowledge
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm install
python scripts/validate_catalog.py
python -m unittest discover -s tests -p 'test_*.py'
python scripts/build_ai_index.py
npm run docs:build
npm run docs:serve
```

Портал будет доступен по адресу `http://localhost:5005`. Для пересборки при изменениях используйте `npm run docs:watch` в отдельном терминале. Команда Diplodoc под npm-скриптом: `yfm build -i . -o _site`.

## Как внести изменения

Следуйте [инструкции для автора](guides/how-to-contribute.md). Перед merge должны успешно пройти валидация, unit-тесты, AI-экспорт и сборка Diplodoc.

## GitHub Pages

Workflow `.github/workflows/catalog.yml` проверяет pull request, а push в `main` дополнительно публикует статический сайт. В настройках репозитория выберите **Settings → Pages → Source: GitHub Actions**. Секреты для сборки не нужны.

## Next steps

### Phase 2

- semantic search;
- embeddings;
- RAG;
- AI chat.

### Phase 3

- MCP server;
- подключение Codex, Claude и Cursor;
- ссылки AI-ответов на конкретные документы.

### Phase 4

- автоматическое извлечение знаний из inbox;
- AI-generated pull requests;
- human review;
- автоматическая проверка устаревших документов.

### Phase 5

- knowledge graph;
- визуализация зависимостей;
- impact analysis: «что затронет изменение данной системы?».

