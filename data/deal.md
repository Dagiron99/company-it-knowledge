---
id: deal
type: data
name: Сделка
description: Демонстрационная коммерческая сделка с клиентом, суммой, ответственным и этапом продаж.
owner: sales-team
business_owner: sales-team
technical_owner: automation-team
criticality: medium
status: production
sensitivity: internal
tags:
  - crm
  - sales
aliases:
  - лид продаж
  - opportunity
keywords:
  - сделка
  - продажа
  - crm
  - клиент
  - этап сделки
source_of_truth: bitrix24
available_via: []
related:
  - bitrix24
questions:
  - Где лежат данные о сделках?
  - Какая система является Source of Truth для сделки?
  - Через какой API получать сделки?
---

# Сделка

{% note info %}

Коммерческая возможность с клиентом, ответственным сотрудником, суммой и текущим этапом воронки.

{% endnote %}

## Паспорт

| Факт | Ответ |
| --- | --- |
| Source of Truth | [Bitrix24](../systems/bitrix24.md) |
| Владелец данных | [Команда продаж](../teams/sales-team.md) |
| Технический владелец | [Отдел автоматизации](../teams/automation-team.md) |
| Чувствительность | `internal`; права зависят от роли и коммерческой конфиденциальности. |
| Рекомендуемый доступ | Способ программного получения в MVP не задокументирован. |
| Не использовать | Неучтённые выгрузки и прямое подключение к хранилищу CRM. |

## Связи и поток данных

**Сделка** хранится в [Bitrix24](../systems/bitrix24.md). Бизнес-правила и состав полей определяет [команда продаж](../teams/sales-team.md).

## Частые вопросы

**Через какой API читать сделки?** Эта информация не задокументирована; каталог не должен придумывать интерфейс.

{% cut "Состав данных" %}

В демонстрационной модели известны `deal_id`, `title`, `customer_id`, `owner_employee_id`, `amount`, `currency` и `stage`.

{% endcut %}

{% cut "Доступ и ограничения" %}

Запросите способ доступа у [команды продаж](../teams/sales-team.md) и [отдела автоматизации](../teams/automation-team.md). Если нужен API, после review добавьте отдельную сущность `service` в каталог.

{% endcut %}
