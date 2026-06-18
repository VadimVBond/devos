# Архитектура ядра DevOS (Core Architecture)

## 1. Структура проекта (Folder Structure)

Платформа строится по принципу **Modular Monolith**.

```text
devos/
├── .ai/                    # Документация и промпты ИИ
│   ├── design/             # Архитектурные решения
│   └── prompts/            # Системные промпты
├── src/
│   └── devos/              # Основной пакет приложения
│       ├── core/           # Ядро системы (не зависит от модулей)
│       │   ├── cli/        # Базовая настройка Typer
│       │   ├── config/     # Pydantic Settings
│       │   ├── events/     # Event Bus (Internal)
│       │   ├── logging/    # Настройка Loguru
│       │   └── storage/    # SQLAlchemy Engine & Session
│       ├── modules/        # Функциональные модули
│       │   ├── project/    # Project Registry
│       │   ├── plugin/     # Plugin Manager
│       │   ├── task/       # Task Manager
│       │   └── ...         # Другие модули
│       ├── shared/         # Общие утилиты и модели данных
│       └── main.py         # Точка входа в CLI
├── tests/                  # Тесты
├── .gitignore
├── pyproject.toml          # Настройки проекта и зависимости
└── README.md
```

## 2. CLI Core Design

Используется **Typer** для создания иерархической структуры команд.

### Базовые группы команд:
*   `devos project`: Управление проектами в реестре.
*   `devos plugin`: Управление плагинами.
*   `devos task`: Мониторинг и запуск задач.
*   `devos worker`: Управление воркерами.
*   `devos workflow`: Работа с воркфлоу (DAG).
*   `devos ai`: Прямое взаимодействие с ИИ роутером.
*   `devos planner`: Создание планов выполнения.

### Системные команды:
*   `devos init`: Инициализация локальной базы данных и конфигурации.
*   `devos doctor`: Проверка окружения (Python version, SQLite, зависимости).

## 3. Storage Layer (Project Registry)

Используется **SQLAlchemy 2.0+** с асинхронным драйвером для SQLite.

### Базовая модель `Project`:
*   `id`: UUID (Primary Key)
*   `name`: String
*   `path`: String (Absolute path to project root)
*   `stack`: String (e.g., "Python/FastAPI")
*   `description`: Text
*   `tags`: JSON/String
*   `status`: Enum (active, archived, etc.)
*   `created_at`: DateTime
*   `updated_at`: DateTime

## 4. Конфигурация (Pydantic Settings)

Настройки хранятся в `.env` файле или переменных окружения.

### Основные параметры:
*   `DEVOS_HOME`: Путь к домашней директории DevOS (по умолчанию `~/.devos`).
*   `DATABASE_URL`: Путь к SQLite БД.
*   `LOG_LEVEL`: Уровень логирования.

## 5. Протоколы и Интерфейсы (Core Interfaces)

Все модули должны следовать единым контрактам для обеспечения слабой связности.

### Пример базового интерфейса модуля:
```python
class BaseModule:
    def initialize(self):
        """Регистрация команд в CLI и слушателей событий."""
        pass
```
