import json
from pathlib import Path
from typing import List, Dict, Any

class MetricsCollector:
    """Aggregates metrics from the event stream / trace logs."""
    
    def __init__(self, log_dir: str = ".runtime/logs/traces"):
        self.log_dir = Path(log_dir)

    def calculate_metrics(self) -> Dict[str, Any]:
        """Reads all traces and calculates required metrics."""
        execution_time_per_node: Dict[str, List[float]] = {}
        plugin_executions: Dict[str, int] = {}
        plugin_failures: Dict[str, int] = {}
        graph_execution_times: List[float] = []

        if not self.log_dir.exists():
            return self._build_empty_metrics()

        for file_path in self.log_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    events = json.load(f)
                    
                for event in events:
                    event_type = event.get("event_type")
                    
                    if event_type == "TaskCompleted":
                        action = event.get("action", "unknown")
                        duration = event.get("duration_ms", 0)
                        
                        execution_time_per_node.setdefault(action, []).append(duration)
                        plugin_executions[action] = plugin_executions.get(action, 0) + 1
                        
                    elif event_type == "TaskFailed":
                        action = event.get("action", "unknown")
                        plugin_executions[action] = plugin_executions.get(action, 0) + 1
                        plugin_failures[action] = plugin_failures.get(action, 0) + 1
                        
                    elif event_type == "GraphCompleted":
                        duration = event.get("duration_ms", 0)
                        graph_execution_times.append(duration)
                        
            except Exception as e:
                pass # Skip corrupted logs
                
        # Aggregate
        avg_exec_per_node = {k: sum(v)/len(v) for k, v in execution_time_per_node.items() if v}
        success_rate = {
            action: ((plugin_executions[action] - plugin_failures.get(action, 0)) / plugin_executions[action]) * 100
            for action in plugin_executions
        }
        avg_graph_time = sum(graph_execution_times) / len(graph_execution_times) if graph_execution_times else 0

        return {
            "execution_time_per_node_ms": avg_exec_per_node,
            "plugin_success_rate_percent": success_rate,
            "failure_rate_per_action": {action: 100 - rate for action, rate in success_rate.items()},
            "average_graph_execution_time_ms": avg_graph_time,
            "total_graphs_executed": len(graph_execution_times)
        }

    def _build_empty_metrics(self) -> Dict[str, Any]:
        return {
            "execution_time_per_node_ms": {},
            "plugin_success_rate_percent": {},
            "failure_rate_per_action": {},
            "average_graph_execution_time_ms": 0,
            "total_graphs_executed": 0
        }
