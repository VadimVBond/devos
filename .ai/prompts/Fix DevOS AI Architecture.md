# 🧠 PROMPT: Fix DevOS AI Architecture (.ai/ vs ai/)

```text
You are refactoring the DevOS project architecture.

Your goal is to strictly separate two layers:

---

# 1. ai/ (Execution Layer - CODE)

This folder is responsible for runtime execution of the system.

It MUST contain ONLY deterministic code.

Responsibilities:
- LLM runtime execution (calls to models)
- routing between AI providers (OpenAI, Ollama, etc.)
- converting prompts into structured outputs
- validation of AI responses
- providing a single entrypoint: ai/runtime.py

STRICT RULES:
- NO prompts stored here (except minimal system wiring)
- NO workflows or agent behavior definitions
- NO experimental logic
- NO business rules outside execution pipeline
- MUST be imported by kernel only via ai/runtime.py

---

# 2. .ai/ (Cognitive Layer - AI BEHAVIOR DEFINITION)

This folder defines HOW the system thinks.

It is NOT executable code.

Responsibilities:
- system prompts (planner, critic, executor)
- agent workflows and reasoning templates
- behavioral rules for AI decision making
- policy instructions for task generation
- experimental AI behavior configurations

STRICT RULES:
- NO Python runtime code
- NO execution logic
- MUST NOT directly call LLM APIs
- MUST be read only by ai/runtime.py or kernel planner
- Acts as “instruction memory” for AI behavior

---

# ARCHITECTURAL PRINCIPLE

ai/ = HOW TO EXECUTE
.ai/ = HOW TO THINK

---

# DATA FLOW (MANDATORY)

1. Kernel receives user input
2. Kernel sends request to ai/runtime.py
3. ai/runtime.py loads relevant prompts from .ai/
4. LLM processes prompt and returns structured JSON
5. Kernel planner converts output into task graph
6. Executor runs plugins
7. Memory layer stores result

---

# CRITICAL CONSTRAINTS

- ai/ and .ai/ MUST NOT overlap responsibilities
- .ai/ MUST NOT contain executable logic
- ai/ MUST NOT contain prompt-heavy behavior definitions
- All AI behavior must be externalized into .ai/
- All execution must stay inside ai/

---

# OUTPUT EXPECTATION

Refactor project so that:
- ai/ becomes pure runtime engine
- .ai/ becomes cognitive instruction layer
- Kernel connects both layers without mixing concerns
```

---

# 🧠 Коротко смысл (чтобы ты зафиксировал модель)

* `ai/` = мотор (исполнение)
* `.ai/` = мозг (поведение)
* `kernel/` = диспетчер (оркестрация)


