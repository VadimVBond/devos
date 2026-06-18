# Архитектура DevOS: Orchestration Layer

## 1. Концепция (Core Idea)

DevOS — это **оркестрационный слой для разработки**, действующий как ядро (Kernel) между пользователем, AI и инструментами.

> **Принцип:** "DevOS does not do work. DevOS orchestrates work."

## 2. Архитектурные слои

### 2.1 Core Engine (Kernel)
Отвечает за логику управления:
*   `engine/`: Координация всех процессов.
*   `planner/`: Создание планов задач на основе интентов.
*   `executor/`: Запуск задач через плагины.
*   `router/`: Маршрутизация запросов.
*   `policy/`: Проверка безопасности и прав доступа.

### 2.2 AI Layer
Абстракция над моделями ИИ:
*   `providers/`: Адаптеры (OpenAI, Claude, Ollama, Gemini).
*   `router/`: Выбор оптимальной модели для конкретной задачи.
*   `prompts/`: Реестр системных промптов.

### 2.3 Memory Layer
Единая система контекста:
*   `storage/`: Долговременная память (SQLite/SQLAlchemy).
*   `context/`: Сессионная и проектная память.

### 2.4 Tooling Layer (Plugins)
Изолированные модули действий. Любой новый функционал = плагин.
*   Контракт: `name`, `description`, `input_schema`, `output_schema`, `run()`.

### 2.5 CLI Layer
Первичный интерфейс взаимодействия. Вызывает Core Engine, не содержит бизнес-логики.

## 3. Структура проекта

```text
src/devos/
├── core/           # Kernel & Logic
├── ai/             # AI Abstraction
├── memory/         # Context & Storage
├── plugins/        # Tools & Actions
├── cli/            # Interface & REPL
├── config/         # Settings
└── shared/         # Common Utilities
```

## 4. Схема выполнения (Execution Pipeline)

1.  **User Input** → CLI
2.  **Intent Resolver** (AI) → Определение намерения.
3.  **Planner** → Генерация графа задач.
4.  **Policy Guard** → Проверка безопасности.
5.  **Execution Engine** → Запуск плагинов.
6.  **Memory Update** → Сохранение результата.
7.  **Response** → Вывод пользователю.
