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

## Назначение

<!-- Для кого и для чего предназначен сервис. -->

## Какие данные предоставляет

<!-- Ссылки на data/. -->

## Откуда получает данные

<!-- Ссылки на systems/. -->

## Протокол и аутентификация

<!-- Protocol, authentication и environments; без endpoint и секретов. -->

## Как получить доступ

<!-- Укажите процесс согласования. -->

## Пример использования

<!-- Без production URL и credentials. -->

## Ограничения

<!-- Лимиты, задержка, недоступные поля. -->

## Владелец и поддержка

<!-- Команда и безопасный канал обращения. -->

