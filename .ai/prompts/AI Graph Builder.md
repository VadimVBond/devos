## TASK: AI Graph Builder

---

# 🧠 PROMPT ДЛЯ СЛЕДУЮЩЕГО ШАГА DEVOS

```text id="x7v9kd"
You are extending DevOS with AI Graph Generation Layer.

GOAL:
Convert natural language intents into Execution Graph (DAG) compatible with Kernel Executor.

---

# REQUIREMENTS

1. Input:
   - user natural language request
   - optional project context

2. Output MUST be ExecutionGraph:

{
  "nodes": [
    {
      "id": "task_1",
      "action": "plugin.method",
      "input": {},
      "depends_on": [],
      "retry": {
        "max_retries": 2
      }
    }
  ],
  "edges": [
    ["task_1", "task_2"]
  ]
}

---

# CORE RULES

- Always decompose complex tasks into subtasks
- Every node must map to a plugin action
- No node can exist without explicit execution purpose
- Dependencies must be explicit (no implicit ordering)
- Avoid single-node graphs for complex requests

---

# AI BEHAVIOR RULES

- Prefer minimal DAG depth
- Group independent tasks in parallel branches
- Split tasks by tool responsibility (fs, git, system, etc.)
- Ensure all nodes are executable by KernelExecutor

---

# VALIDATION RULES

Reject output if:
- node has no plugin action
- dependency references non-existent node
- graph contains cycles
- task is too abstract (not executable)

---

# GOAL OUTPUT

Transform any user request into a valid DevOS Execution Graph.
```

---


