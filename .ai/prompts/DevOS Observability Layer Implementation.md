You are working on DevOS — an AI-powered execution orchestration system based on:
- Kernel execution engine
- DAG-based task graphs
- Plugin system (fs, git, etc.)
- AI Planner generating ExecutionGraphs

Your task is to implement an Observability Layer for the DevOS Kernel without modifying core execution logic.

---

# GOAL

Add full visibility into execution of DevOS DAG system.

The system must become fully traceable, debuggable, and replayable.

---

# REQUIRED COMPONENTS

## 1. Execution Trace System

Track every node in the Execution Graph:

Each execution must log:
- node_id
- action (plugin.method)
- input
- output
- status (pending / running / success / failed / skipped)
- start_time
- end_time
- duration
- error (if any)

---

## 2. Event Logger (Core Requirement)

Implement event-based logging inside KernelExecutor:

Events:
- task_started
- task_completed
- task_failed
- task_skipped
- graph_started
- graph_completed

All events must be stored in structured format (JSON).

---

## 3. Execution Replay System

Add ability to:
- replay full DAG execution from logs
- replay single node execution
- reproduce past execution state deterministically

---

## 4. Debug Mode

Add a debug layer that provides:

- explanation why a node executed
- explanation why a node was skipped
- dependency resolution trace
- failure propagation trace

---

## 5. Metrics Collection

Collect system metrics:

- execution_time_per_node
- plugin_success_rate
- failure_rate_per_action
- average_graph_execution_time

---

# ARCHITECTURAL RULES

- Observability must NOT modify execution logic
- It must wrap KernelExecutor (decorator / middleware pattern)
- No plugin is allowed to bypass observability layer
- DAG structure must remain unchanged
- Logging must be non-blocking (async or buffered)

---

# IMPLEMENTATION REQUIREMENTS

Create new module:

kernel/observability/

Suggested structure:

- tracer.py        → execution tracking
- events.py        → event definitions
- logger.py        → structured logging system
- replay.py        → replay engine
- metrics.py       → metrics collector

---

# INTEGRATION POINT

Modify KernelExecutor:

Wrap execution like:

execute_node(node) → observability.trace(node) → execute → log result

---

# OUTPUT EXPECTATION

Return:

1. Updated architecture
2. Code-level implementation
3. Integration strategy with DAG executor
4. Example execution trace output (JSON)

---

# GOAL

Make DevOS fully observable, debuggable, and replayable like production-grade orchestration systems (Temporal / Airflow-like visibility layer).