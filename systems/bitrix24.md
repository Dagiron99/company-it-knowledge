---
id: bitrix24
type: system
name: Bitrix24
description: Демонстрационный корпоративный портал и CRM для сделок, задач и отображения части данных сотрудников.
owner: automation-team
business_owner: sales-team
technical_owner: automation-team
criticality: high
status: production
tags:
  - crm
  - portal
aliases:
  - Битрикс
  - корпоративный портал
keywords:
  - битрикс
  - crm
  - сделки
  - задачи
  - сотрудники
contains:
  - deal
  - employee
provides_services: []
integrates_with:
  - 1c-zup
  - active-directory
related:
  - zup-to-bitrix
questions:
  - Кто отвечает за Bitrix24?
  - Является ли Bitrix24 источником истины для сотрудников?
  - Откуда Bitrix24 получает организационную структуру?
---

# Bitrix24

{% note info %}

Демонстрационный корпоративный портал и CRM: здесь ведутся сделки, задачи и отображается копия части кадровых сведений.

{% endnote %}

## Паспорт

| Факт | Ответ |
| --- | --- |
| Назначение | CRM для сделок и портал для задач и поиска коллег. |
| Source of Truth | Для [сделки](../data/deal.md). |
| Кадровые данные | Только копия ФИО, отдела, должности и руководителя из 1С ЗУП. |
| Бизнес-владелец | [Команда продаж](../teams/sales-team.md) |
| Технический владелец | [Отдел автоматизации](../teams/automation-team.md) |
| Доступ | Для кадровых данных — [Employee API](../services/employee-api.md); API сделок в MVP не задокументирован. |

## Связи и поток данных

[1С ЗУП](1c-zup.md) → [синхронизация каждые 15 минут](../integrations/zup-to-bitrix.md) → **Bitrix24**.

Учётные записи сопоставляются с [Active Directory](active-directory.md). Кадровый профиль в Bitrix24 не должен использоваться как первичный источник.

## Частые вопросы

**Где взять руководителя сотрудника?** Через Employee API, а не из Bitrix24.

**Где лежат данные о сделках?** Source of Truth для сделки — Bitrix24.

{% cut "Доступ и ограничения" %}

Кадровая копия обновляется каждые 15 минут и может отставать от Source of Truth. Доступ к CRM запрашивается по [общей инструкции](../guides/how-to-get-access.md).

В каталоге нет production URL, токенов и реальных учётных данных.

{% endcut %}

{% cut "Эксплуатация" %}

За техническую часть Bitrix24 отвечает [отдел автоматизации](../teams/automation-team.md), за CRM-процесс и данные сделок — [команда продаж](../teams/sales-team.md).

{% endcut %}
