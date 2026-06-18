import time
import inspect
import asyncio
from typing import Dict, Any, Optional
from plugins.registry import PluginRegistry
from kernel.observability.logger import AsyncEventLogger
from kernel.observability.events import (
    TaskStarted, TaskCompleted, TaskFailed, GraphStarted, GraphCompleted
)
from loguru import logger

class ExecutionTracer:
    """
    Wrapper for PluginRegistry that intercepts execution calls to emit trace events.
    Matches the pattern: KernelExecutor -> ExecutionTracer -> PluginRegistry.
    """
    
    def __init__(self, registry: PluginRegistry, event_logger: AsyncEventLogger):
        self.registry = registry
        self.logger = event_logger
        self.current_graph_id: str = "unknown"
        
    def list_plugins(self):
        return self.registry.list_plugins()
        
    def get_plugin(self, name: str):
        return self.registry.get_plugin(name)

    def execute(self, name: str, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Intercepts plugin execution and extracts trace context.
        Uses explicit context instead of stack inspection for deterministic behavior.
        """
        task_id = context.get("task_id", -1) if context else -1
        
        # We need to run the async logging. Since execute() is sync, we use a background task or run it if event loop is running.
        # But for simplicity, we'll just queue the event directly to logger buffer inside a try/except to avoid blocking.
        
        start_time = time.time()
        
        task_started = TaskStarted(
            graph_id=self.current_graph_id,
            task_id=task_id,
            action=name,
            input_data=params
        )
        self._sync_log(task_started)
        
        try:
            result = self.registry.execute(name, params, context=context)
            
            duration_ms = (time.time() - start_time) * 1000
            task_completed = TaskCompleted(
                graph_id=self.current_graph_id,
                task_id=task_id,
                action=name,
                output_data=result,
                duration_ms=duration_ms
            )
            self._sync_log(task_completed)
            return result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            task_failed = TaskFailed(
                graph_id=self.current_graph_id,
                task_id=task_id,
                action=name,
                error=str(e),
                duration_ms=duration_ms
            )
            self._sync_log(task_failed)
            raise
        
    def _sync_log(self, event):
        """Helper to synchronously add event to the logger buffer."""
        self.logger._buffer.append(event)
        logger.debug(f"Event logged: {event.event_type} [{event.event_id}]")

class ObservableGraphExecutor:
    """
    Wraps the execute_plan call to capture GraphStarted and GraphCompleted.
    """
    def __init__(self, executor, tracer: ExecutionTracer):
        self.executor = executor
        self.tracer = tracer
        
        # Inject tracer as the registry
        self.executor.registry = self.tracer

    async def execute_plan(self, plan):
        import uuid
        graph_id = str(uuid.uuid4())
        self.tracer.current_graph_id = graph_id
        
        graph_started = GraphStarted(
            graph_id=graph_id,
            intent=plan.intent if hasattr(plan, 'intent') else "Unknown intent"
        )
        await self.tracer.logger.log_event(graph_started)
        
        start_time = time.time()
        try:
            result = await self.executor.execute_plan(plan)
            
            graph_completed = GraphCompleted(
                graph_id=graph_id,
                duration_ms=(time.time() - start_time) * 1000,
                status="success"
            )
            await self.tracer.logger.log_event(graph_completed)
            return result
        except Exception as e:
            graph_completed = GraphCompleted(
                graph_id=graph_id,
                duration_ms=(time.time() - start_time) * 1000,
                status="failed"
            )
            await self.tracer.logger.log_event(graph_completed)
            raise
        finally:
            await self.tracer.logger.flush(graph_id)
