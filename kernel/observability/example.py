import asyncio
import json
from kernel.executor import KernelExecutor
from kernel.planner import ExecutionPlan, ExecutionGraph, TaskNode
from plugins.registry import PluginRegistry
from kernel.observability import (
    AsyncEventLogger, 
    ExecutionTracer, 
    ObservableGraphExecutor,
    MetricsCollector,
    ExecutionReplayer
)

async def main():
    # 1. Base Setup
    registry = PluginRegistry()
    executor = KernelExecutor(registry=registry) # It doesn't matter what registry we pass here because it gets overwritten by the wrapper
    
    # 2. Setup Observability Layer
    event_logger = AsyncEventLogger(log_dir=".runtime/logs/traces")
    tracer = ExecutionTracer(registry=registry, event_logger=event_logger)
    
    # 3. Wrap Executor
    observable_executor = ObservableGraphExecutor(executor=executor, tracer=tracer)
    
    # 4. Create dummy plan
    graph = ExecutionGraph()
    node1 = TaskNode(id=1, action="fs.exists", input={"path": "."})
    node2 = TaskNode(id=2, action="fs.ls", input={"path": "."})
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_edge(1, 2)
    
    plan = ExecutionPlan(intent="List current directory if exists", graph=graph)
    
    # 5. Execute Plan (This will automatically generate traces)
    print("Executing Plan...")
    await observable_executor.execute_plan(plan)
    
    # 6. Generate Metrics Example
    print("\nGenerating Metrics...")
    metrics_collector = MetricsCollector(log_dir=".runtime/logs/traces")
    metrics = metrics_collector.calculate_metrics()
    print(json.dumps(metrics, indent=2))
    
    # 7. Generate Replay Example
    print("\nReplaying Trace...")
    # Get the latest trace file
    import os
    from pathlib import Path
    traces_dir = Path(".runtime/logs/traces")
    trace_files = list(traces_dir.glob("*.json"))
    if trace_files:
        latest_trace = max(trace_files, key=os.path.getctime)
        replayer = ExecutionReplayer(trace_file=str(latest_trace), registry=registry)
        replayer.replay_full_dag()

if __name__ == "__main__":
    asyncio.run(main())
