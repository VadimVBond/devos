## 👉 TASK: “Introduce Execution Graph Layer”

---

# 🧠 PROMPT ДЛЯ СЛЕДУЮЩЕГО ЭТАПА DEVOS

(можешь прямо вставить в систему)

```text
You are upgrading DevOS Kernel to support Execution Graph Layer.

GOAL:
Introduce a deterministic execution model between Planner and Executor.

---

# REQUIREMENTS

1. Replace linear task execution with DAG (Directed Acyclic Graph)
2. Each task must support:
   - id
   - action (plugin.method)
   - input
   - dependencies (depends_on)
   - state (pending/running/success/failed/skipped)

3. Add Execution State Manager:
   - tracks task lifecycle
   - prevents execution of unresolved dependencies

4. Add Retry Policy:
   - retry_failed_tasks: true/false
   - max_retries: integer

5. Add Failure Propagation Rules:
   - if parent task fails → dependent tasks are skipped

---

# MODIFICATIONS

- kernel/planner.py → output DAG instead of flat list
- kernel/executor.py → graph-aware execution
- kernel/state.py → new module for execution tracking

---

# OUTPUT FORMAT

Planner must now return:

{
  "intent": "...",
  "graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

---

