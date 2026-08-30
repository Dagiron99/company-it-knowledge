---
id: employee
type: data
name: Сотрудник
description: Основная информация о сотруднике, его должности, подразделении, руководителе и кадровом статусе.
owner: hr-team
business_owner: hr-team
technical_owner: automation-team
criticality: high
status: production
sensitivity: personal_data
tags:
  - hr
  - personal-data
aliases:
  - работник
  - employee
keywords:
  - сотрудник
  - работник
  - ФИО
  - руководитель
  - начальник
  - подразделение
  - отдел
  - должность
  - employee
  - manager
  - department
source_of_truth: 1c-zup
available_via:
  - employee-api
related:
  - bitrix24
  - active-directory
  - zup-to-bitrix
questions:
  - Где получить данные сотрудника?
  - Где определить руководителя сотрудника?
  - Где взять подразделение или отдел сотрудника?
  - Как получить ФИО сотрудника по ID?
---

# Сотрудник

{% note info %}

Работник компании со стабильным `employee_id`: ФИО, должность, отдел, руководитель и кадровый статус.

{% endnote %}

## Паспорт

| Факт | Ответ |
| --- | --- |
| Source of Truth | [1С ЗУП](../systems/1c-zup.md) |
| Рекомендуемый доступ | [Employee API](../services/employee-api.md) |
| Владелец данных | [HR-команда](../teams/hr-team.md) |
| Технический владелец | [Отдел автоматизации](../teams/automation-team.md) |
| Чувствительность | `personal_data`; доступ по минимальным привилегиям. |
| Не использовать как источник | Bitrix24, Active Directory, ручные выгрузки и прямую базу 1С. |

## Связи и поток данных

**Сотрудник** → [1С ЗУП](../systems/1c-zup.md) → [Employee API](../services/employee-api.md) → потребители.

Ограниченная копия профиля передаётся в [Bitrix24](../systems/bitrix24.md) по [интеграции ЗУП → Bitrix24](../integrations/zup-to-bitrix.md). Active Directory содержит технические атрибуты, а не кадровую истину.

## Частые вопросы

**Где получить руководителя, начальника или подразделение сотрудника?** В Employee API по `employee_id`.

**Что делать, если API не содержит нужного поля?** Обратиться к владельцу и считать поле незадокументированным до обновления каталога.

{% cut "Состав данных" %}

| Поле | Смысл |
| --- | --- |
| `employee_id` | Стабильный идентификатор. |
| `full_name` | ФИО. |
| `department` | Подразделение или отдел. |
| `manager_id` | Руководитель или начальник. |
| `position` | Должность. |
| `employment_status` | Кадровый статус. |

{% endcut %}

{% cut "Доступ и ограничения" %}

Employee API возвращает разрешённое подмножество данных и не публикует зарплату или документы сотрудника. Не читайте кадровые сведения из копий: они могут быть неполными или устаревшими.

{% endcut %}
