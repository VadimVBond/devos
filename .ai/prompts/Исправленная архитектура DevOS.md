# 🔧 Исправленная архитектура DevOS (как промпт/спека)

Ниже — переработанный “system prompt / architecture spec”, который можно использовать как основу репозитория и CLI/AI-ядра.

---

# DevOS — AI Developer Operating Layer (Re-Architecture Prompt)

## 1. Система (Core Idea)

DevOS — это **оркестрационный слой для разработки**, который объединяет:

* локальный CLI агент
* AI-планировщик задач
* контекстную память
* плагины действий (git, fs, docker, api)
* UI dashboard (опционально)

❗ DevOS НЕ является:

* ОС
* автономным агентом без контроля
* UI-приложением в первую очередь

---

## 2. Архитектурные уровни

### 2.1 Core Engine (DevOS Kernel Layer)

Отвечает за:

* интерпретацию команд
* маршрутизацию задач
* execution pipeline
* безопасность (sandbox rules)
* tool registry

**Слои внутри Core:**

* Command Parser
* Intent Resolver (LLM optional)
* Task Planner
* Execution Engine
* Policy Guard
* Event Bus

---

### 2.2 Memory Layer

Единая контекстная система:

* session memory
* project memory
* long-term SQLite storage
* embeddings index (optional)

Хранит:

* проекты
* команды
* ошибки
* действия
* пользовательские предпочтения

---

### 2.3 Tooling Layer (Plugins)

Каждый инструмент — изолированный модуль:

* git-tools
* fs-tools
* docker-tools
* python-runtime-tools
* api-connectors
* code-analyzers

Правило:

> любой новый функционал = plugin, а не изменение ядра

---

### 2.4 AI Layer

Абстракция над LLM:

* OpenAI / Claude / local Ollama
* routing моделей по задачам
* fallback logic
* prompt templates registry

Функции:

* intent understanding
* plan generation
* error explanation
* code suggestion

---

### 2.5 CLI Layer (Primary Interface)

CLI — главный вход в систему:

```
devos> init project fastapi
devos> analyze current repo
devos> fix build errors
devos> plan feature authentication
```

CLI НЕ содержит бизнес-логики — только вызывает Core Engine.

---

### 2.6 UI Layer (Secondary)

Web dashboard (React / Vite):

* визуализация задач
* memory timeline
* AI coach output
* project graphs

❗ UI не управляет системой напрямую — только читает Core API

---

## 3. Execution Model

Каждая команда проходит pipeline:

```
User Input
   ↓
Command Parser
   ↓
Intent Resolver (AI optional)
   ↓
Planner (creates structured tasks)
   ↓
Policy Guard (security check)
   ↓
Execution Engine
   ↓
Tool Plugins
   ↓
Memory Store update
   ↓
Response output
```

---

## 4. Plugin Contract (важно)

Каждый plugin обязан иметь:

```python
{
  "name": "git.commit",
  "description": "...",
  "input_schema": {},
  "output_schema": {},
  "run(context) -> result"
}
```

---

## 5. DevOS CLI structure (реальная папка)

```
devos/
  core/
    engine/
    planner/
    executor/
    router/
    policy/

  ai/
    providers/
    prompts/
    router/

  memory/
    sqlite/
    embeddings/

  plugins/
    git/
    fs/
    docker/
    system/

  cli/
    commands/
    repl.py
    parser.py

  ui/   (optional)
    dashboard/

  config/
    settings.json
```

---

## 6. Ключевое исправление концепта (очень важно)

### ❌ Было:

“DevOS = AI OS + CLI + dashboard + Notion + everything”

### ✅ Стало:

DevOS = **Kernel + plugin runtime + AI planner**

---

## 7. Как теперь правильно позиционировать репозитории

### repo split (рекомендуется)

1. `devos-core`

   * engine
   * memory
   * planner
   * plugins runtime

2. `devos-cli`

   * CLI interface
   * REPL
   * command bindings

3. `devos-ui`

   * React dashboard
   * visualization only

---

## 8. Главный architectural принцип

> "DevOS does not do work. DevOS orchestrates work."

---
