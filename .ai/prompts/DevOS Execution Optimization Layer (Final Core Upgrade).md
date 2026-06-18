You are designing the Execution Optimization Layer for DevOS — a deterministic AI orchestration system with:

- AI Planner (NL → ExecutionGraph)
- Critic Engine (validation + safety gate)
- KernelExecutor (DAG execution engine)
- Observability Layer (tracing + metrics)
- Feedback Layer (bounded memory signals)

Now we introduce a new layer: EXECUTION OPTIMIZER.

---

# GOAL

Optimize ExecutionGraph BEFORE execution in terms of:

1. Performance (parallelism, execution speed)
2. Cost (minimize expensive operations)
3. Resource efficiency (plugin execution ordering)
4. Graph structure simplification

---

# POSITION IN PIPELINE

Final pipeline:

AI Planner
   ↓
Critic Engine (hard safety gate)
   ↓
Execution Optimizer (NEW)
   ↓
KernelExecutor
   ↓
Observability
   ↓
Feedback Loop

---

# CORE RESPONSIBILITIES

## 1. DAG PARALLELIZATION ANALYSIS

Detect independent nodes and:
- group into execution batches
- maximize parallel execution opportunities
- remove unnecessary sequential constraints

---

## 2. COST OPTIMIZATION

Assign cost weights to actions:

Examples:
- fs.read → low cost
- fs.write → medium cost
- git operations → medium/high cost
- external API calls → high cost

Optimizer must:
- reorder execution to reduce peak cost
- delay expensive operations when possible
- cluster cheap operations first

---

## 3. GRAPH SIMPLIFICATION

Detect and remove:
- redundant nodes
- duplicate actions
- no-op steps
- unnecessary dependency chains

Merge where possible:
- identical actions with same inputs
- sequential fs operations into batch operations (if safe)

---

## 4. EXECUTION BATCH GENERATION

Transform DAG into:

execution_batches = [
  [node1, node2, node3],  # parallel batch
  [node4],
  [node5, node6]
]

Each batch MUST respect dependency constraints.

---

## 5. PREDICTIVE BOTTLENECK DETECTION

Identify:
- slow plugin chains
- dependency-heavy paths
- high-risk execution branches

Annotate graph with:
- "bottleneck_score"
- "execution_risk"

---

# STRICT RULES

- Optimizer MUST NOT change semantic meaning of graph
- Optimizer MUST NOT introduce new tasks
- Optimizer MUST NOT remove safety-critical steps
- Optimizer MUST preserve Critic Engine decisions
- Optimizer MUST remain deterministic (no randomness)

---

# INPUT / OUTPUT CONTRACT

Input:
ExecutionGraph (validated by CriticEngine)

Output:
OptimizedExecutionGraph {
  original_graph,
  optimized_graph,
  execution_batches,
  cost_analysis,
  performance_score,
  changes_log
}

---

# MODULE STRUCTURE

Create:

kernel/optimizer/

Files:
- optimizer_engine.py → main orchestrator
- parallel_analyzer.py → dependency + concurrency detection
- cost_model.py → cost estimation per plugin/action
- graph_rewriter.py → safe graph transformation
- bottleneck_detector.py → performance analysis

---

# INTEGRATION POINT

Pipeline becomes:

AIPlanner → CriticEngine → ExecutionOptimizer → KernelExecutor

Optimizer runs ONLY after Critic approval.

---

# OUTPUT REQUIREMENTS

Return:

1. Optimized architecture diagram
2. Execution batching strategy
3. Cost model definition
4. Example optimized graph transformation
5. Safety guarantees (no semantic drift)

---

# GOAL

Transform DevOS from:
"correct execution system"

into:
"performance-aware deterministic execution runtime with AI planning"