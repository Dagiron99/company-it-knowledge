# Карта связей

{% note info %}

Эта страница создаётся автоматически из YAML-связей доверенных сущностей. Редактируйте поля в `systems/`, `data/`, `services/`, `integrations/` и `teams/`; Mermaid-схемы пересоберутся вместе с порталом.

{% endnote %}

## Потоки данных

```mermaid
flowchart LR
n_deal["Сделка"]
n_employee["Сотрудник"]
n_zup_to_bitrix["Синхронизация сотрудников 1С ЗУП → Bitrix24"]
n_employee_api["Employee API"]
n_1c_zup["1С Зарплата и управление персоналом"]
n_active_directory["Active Directory"]
n_bitrix24["Bitrix24"]
n_automation_team["Отдел автоматизации"]
n_hr_team["HR-команда"]
n_sales_team["Команда продаж"]
class n_deal data;
class n_employee data;
class n_zup_to_bitrix integration;
class n_employee_api service;
class n_1c_zup system;
class n_active_directory system;
class n_bitrix24 system;
class n_automation_team team;
class n_hr_team team;
class n_sales_team team;
n_1c_zup -->|Source of Truth| n_employee
n_1c_zup -->|Синхронизация сотрудников 1С ЗУП → Bitrix24; every-15-minutes| n_bitrix24
n_1c_zup -->|источник API| n_employee_api
n_bitrix24 -->|Source of Truth| n_deal
n_employee -->|доступ через| n_employee_api
n_employee_api -->|предоставляет| n_employee
classDef system fill:#e8f2ff,stroke:#2563a8,stroke-width:2px;
classDef data fill:#eef8f2,stroke:#2f855a,stroke-width:2px;
classDef service fill:#f3efff,stroke:#7252b6,stroke-width:2px;
classDef integration fill:#fff6e5,stroke:#b7791f,stroke-width:2px;
classDef team fill:#f5f6f8,stroke:#596273,stroke-width:2px;
classDef guide fill:#f5f6f8,stroke:#596273,stroke-width:2px;
```

## Владельцы

```mermaid
flowchart LR
n_deal["Сделка"]
n_employee["Сотрудник"]
n_zup_to_bitrix["Синхронизация сотрудников 1С ЗУП → Bitrix24"]
n_employee_api["Employee API"]
n_1c_zup["1С Зарплата и управление персоналом"]
n_active_directory["Active Directory"]
n_bitrix24["Bitrix24"]
n_automation_team["Отдел автоматизации"]
n_hr_team["HR-команда"]
n_sales_team["Команда продаж"]
class n_deal data;
class n_employee data;
class n_zup_to_bitrix integration;
class n_employee_api service;
class n_1c_zup system;
class n_active_directory system;
class n_bitrix24 system;
class n_automation_team team;
class n_hr_team team;
class n_sales_team team;
n_1c_zup -. бизнес-владелец .-> n_hr_team
n_1c_zup -. владелец .-> n_hr_team
n_1c_zup -. технический владелец .-> n_automation_team
n_active_directory -. бизнес-владелец .-> n_automation_team
n_active_directory -. владелец .-> n_automation_team
n_active_directory -. технический владелец .-> n_automation_team
n_bitrix24 -. бизнес-владелец .-> n_sales_team
n_bitrix24 -. владелец .-> n_automation_team
n_bitrix24 -. технический владелец .-> n_automation_team
n_deal -. бизнес-владелец .-> n_sales_team
n_deal -. владелец .-> n_sales_team
n_deal -. технический владелец .-> n_automation_team
n_employee -. бизнес-владелец .-> n_hr_team
n_employee -. владелец .-> n_hr_team
n_employee -. технический владелец .-> n_automation_team
n_employee_api -. бизнес-владелец .-> n_hr_team
n_employee_api -. владелец .-> n_automation_team
n_employee_api -. технический владелец .-> n_automation_team
n_hr_team -. технический владелец .-> n_automation_team
n_sales_team -. технический владелец .-> n_automation_team
n_zup_to_bitrix -. бизнес-владелец .-> n_hr_team
n_zup_to_bitrix -. владелец .-> n_automation_team
n_zup_to_bitrix -. технический владелец .-> n_automation_team
classDef system fill:#e8f2ff,stroke:#2563a8,stroke-width:2px;
classDef data fill:#eef8f2,stroke:#2f855a,stroke-width:2px;
classDef service fill:#f3efff,stroke:#7252b6,stroke-width:2px;
classDef integration fill:#fff6e5,stroke:#b7791f,stroke-width:2px;
classDef team fill:#f5f6f8,stroke:#596273,stroke-width:2px;
classDef guide fill:#f5f6f8,stroke:#596273,stroke-width:2px;
```

## Состав систем и интеграции

```mermaid
flowchart LR
n_deal["Сделка"]
n_employee["Сотрудник"]
n_zup_to_bitrix["Синхронизация сотрудников 1С ЗУП → Bitrix24"]
n_employee_api["Employee API"]
n_1c_zup["1С Зарплата и управление персоналом"]
n_active_directory["Active Directory"]
n_bitrix24["Bitrix24"]
n_automation_team["Отдел автоматизации"]
n_hr_team["HR-команда"]
n_sales_team["Команда продаж"]
class n_deal data;
class n_employee data;
class n_zup_to_bitrix integration;
class n_employee_api service;
class n_1c_zup system;
class n_active_directory system;
class n_bitrix24 system;
class n_automation_team team;
class n_hr_team team;
class n_sales_team team;
n_1c_zup -->|предоставляет сервис| n_employee_api
n_1c_zup -->|содержит| n_employee
n_1c_zup -. интегрируется .-> n_active_directory
n_1c_zup -. интегрируется .-> n_bitrix24
n_active_directory -->|содержит| n_employee
n_active_directory -. интегрируется .-> n_1c_zup
n_active_directory -. интегрируется .-> n_bitrix24
n_bitrix24 -->|содержит| n_deal
n_bitrix24 -->|содержит| n_employee
n_bitrix24 -. интегрируется .-> n_1c_zup
n_bitrix24 -. интегрируется .-> n_active_directory
classDef system fill:#e8f2ff,stroke:#2563a8,stroke-width:2px;
classDef data fill:#eef8f2,stroke:#2f855a,stroke-width:2px;
classDef service fill:#f3efff,stroke:#7252b6,stroke-width:2px;
classDef integration fill:#fff6e5,stroke:#b7791f,stroke-width:2px;
classDef team fill:#f5f6f8,stroke:#596273,stroke-width:2px;
classDef guide fill:#f5f6f8,stroke:#596273,stroke-width:2px;
```

## Как читать схему

- Синие блоки — системы, зелёные — данные, фиолетовые — сервисы, жёлтые — интеграции, серые — команды.
- Сплошная стрелка показывает поток, состав или предоставление данных; пунктирная — владение или интеграционную связь.
- Если связь не записана в YAML, на схеме её нет: генератор не делает предположений.
