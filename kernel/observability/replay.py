import json
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
from plugins.registry import PluginRegistry

class ExecutionReplayer:
    """
    Reads a trace JSON and allows deterministic re-execution
    or simulation of a past DAG execution.
    """
    
    def __init__(self, trace_file: str, registry: PluginRegistry):
        self.trace_file = Path(trace_file)
        self.registry = registry
        self.events: List[Dict[str, Any]] = []
        self._load_trace()

    def _load_trace(self):
        if not self.trace_file.exists():
            raise FileNotFoundError(f"Trace file {self.trace_file} not found.")
            
        with open(self.trace_file, "r", encoding="utf-8") as f:
            self.events = json.load(f)
            
    def get_node_inputs(self, task_id: int) -> Dict[str, Any]:
        """Find the original input data for a given task."""
        for event in self.events:
            if event.get("event_type") == "TaskStarted" and event.get("task_id") == task_id:
                return event.get("input_data", {})
        return {}

    def get_node_action(self, task_id: int) -> str:
        """Find the original action name for a given task."""
        for event in self.events:
            if event.get("event_type") == "TaskStarted" and event.get("task_id") == task_id:
                return event.get("action", "")
        return ""

    def replay_node(self, task_id: int) -> Dict[str, Any]:
        """Re-executes a single node exactly as it was executed before."""
        action = self.get_node_action(task_id)
        inputs = self.get_node_inputs(task_id)
        
        if not action:
            logger.error(f"Cannot replay task {task_id}: action not found in trace.")
            return {}
            
        logger.info(f"Replaying task {task_id} ({action}) with inputs: {inputs}")
        return self.registry.execute(action, inputs)

    def replay_full_dag(self):
        """Re-executes all successful nodes in the trace in sequential order."""
        logger.info(f"Starting full DAG replay from {self.trace_file}")
        
        # We only care about TaskStarted, since it has the inputs
        # But we only want to replay nodes that were actually executed.
        started_tasks = [e for e in self.events if e.get("event_type") == "TaskStarted"]
        
        for task_event in started_tasks:
            task_id = task_event.get("task_id")
            action = task_event.get("action")
            inputs = task_event.get("input_data")
            
            logger.info(f"[REPLAY] Executing {action} (Task {task_id})")
            try:
                result = self.registry.execute(action, inputs)
                logger.success(f"[REPLAY] Success: {result}")
            except Exception as e:
                logger.error(f"[REPLAY] Task {task_id} failed during replay: {e}")
                
        logger.info("Full DAG replay finished.")
