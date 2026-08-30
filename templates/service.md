---
id: example-service
type: service
name: Название сервиса
description: Кратко опишите поддерживаемый интерфейс.
owner: example-team
technical_owner: example-team
business_owner: example-team
criticality: medium
status: draft
protocol: REST
authentication: service-token
environments:
  - test
provides:
  - example-data
source_systems:
  - example-system
depends_on: []
aliases:
  - Альтернативное название API
keywords:
  - естественный запрос api
questions:
  - Какие данные предоставляет сервис?
  - Как получить доступ?
---

# Название сервиса

{% note info %}

<!-- Одно предложение: для кого и для чего предназначен сервис. -->

{% endnote %}

## Паспорт

| Факт | Ответ |
| --- | --- |
| Предоставляет | <!-- Ссылки на data/. --> |
| Источник данных | <!-- Ссылки на systems/. --> |
| Протокол | <!-- Protocol. --> |
| Аутентификация | <!-- Authentication. --> |
| Владелец | <!-- Команда. --> |
| Доступ | <!-- Процесс согласования и environments. --> |

## Связи и поток данных

<!-- Откуда и к кому проходят данные. -->

## Частые вопросы

<!-- Подтверждаемые ответы из questions. -->

{% cut "Доступ и пример использования" %}

<!-- Без production URL и credentials. -->

{% endcut %}

{% cut "Ограничения и эксплуатация" %}

<!-- Лимиты, задержка, недоступные поля и безопасный канал поддержки. -->

{% endcut %}
