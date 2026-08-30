---
id: employee-api
type: service
name: Employee API
description: Демонстрационный корпоративный REST API для безопасного чтения разрешённых данных сотрудников.
owner: automation-team
business_owner: hr-team
technical_owner: automation-team
criticality: high
status: production
protocol: REST
authentication: service-token
environments:
  - test
  - production
provides:
  - employee
source_systems:
  - 1c-zup
depends_on:
  - 1c-zup
aliases:
  - API сотрудников
  - кадровый API
keywords:
  - employee api
  - сотрудники api
  - руководитель api
  - подразделение api
questions:
  - Через какой API получать данные сотрудников?
  - Кто отвечает за Employee API?
  - Откуда Employee API получает информацию?
  - Как получить доступ к Employee API?
---

# Employee API

{% note info %}

Рекомендуемый корпоративный REST API для безопасного чтения разрешённых данных сотрудников.

{% endnote %}

## Паспорт

| Факт | Ответ |
| --- | --- |
| Предоставляет | [Сотрудник](../data/employee.md): ID, ФИО, отдел, `manager_id`, должность и статус. |
| Источник данных | [1С ЗУП](../systems/1c-zup.md), не Bitrix24. |
| Протокол | REST over HTTPS |
| Аутентификация | Service token, выданный конкретному приложению. |
| Владелец | [Отдел автоматизации](../teams/automation-team.md); бизнес-владелец данных — [HR-команда](../teams/hr-team.md). |
| Доступ | По [инструкции](../guides/how-to-get-access.md), для `test` или `production`. |

## Связи и поток данных

[1С ЗУП](../systems/1c-zup.md) → **Employee API** → потребители [данных сотрудника](../data/employee.md).

API скрывает детали подключения к кадровой системе и выдаёт только разрешённое подмножество атрибутов.

## Частые вопросы

**Как получить руководителя сотрудника?** Прочитать `manager_id` через Employee API.

**Что делать, если поля нет?** Считать его незадокументированным и запросить дополнение каталога у владельца.

{% cut "Доступ и пример использования" %}

Укажите сервис-потребитель, окружение, поля, цель использования и ожидаемую нагрузку. Концептуальный запрос — получить сотрудника по `employee_id`.

Конкретный endpoint, URL, токены и credentials не публикуются в каталоге; после выдачи доступа они передаются через утверждённый защищённый канал.

{% endcut %}

{% cut "Ограничения и эксплуатация" %}

API предназначен преимущественно для чтения. Зарплата, документы и другие избыточные персональные данные не возвращаются. Кэш может давать небольшую задержку после изменения в 1С ЗУП.

{% endcut %}
