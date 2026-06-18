import asyncio
from typing import Dict, Any, List
from loguru import logger
from kernel.state import ExecutionStateManager, TaskStatus
from kernel.planner import ExecutionPlan, TaskNode

class KernelExecutor:
    """
    Исполнитель графа задач (Graph-Aware Executor).
    Управляет запуском задач с учетом зависимостей и повторных попыток.
    """
    
    def __init__(self):
        logger.info("Kernel Executor initialized.")

    async def execute_plan(self, plan: ExecutionPlan):
        """Выполняет план, обходя DAG."""
        manager = ExecutionStateManager(
            nodes=plan.graph.nodes, 
            edges=plan.graph.edges
        )
        
        logger.info(f"Starting execution for intent: {plan.intent}")
        
        while True:
            ready_task_ids = manager.get_ready_tasks()
            
            if not ready_task_ids:
                # Проверяем, есть ли еще задачи в работе или ожидании
                pending_tasks = [tid for tid, status in manager.state.task_statuses.items() 
                                if status == TaskStatus.PENDING]
                if not pending_tasks:
                    break
                else:
                    # Если есть PENDING, но нет READY, значит мы в тупике (или ждем async)
                    # В данной реализации мы идем последовательно.
                    break

            # Запускаем готовые задачи (можно параллельно через asyncio.gather)
            for task_id in ready_task_ids:
                task_node = manager.nodes[task_id]
                await self._run_task(task_node, manager)

        logger.success("Execution graph processing finished.")
        return manager.state

    async def _run_task(self, task: TaskNode, manager: ExecutionStateManager):
        """Выполняет конкретную задачу с учетом Retry Policy."""
        manager.update_task_status(task.id, TaskStatus.RUNNING)
        
        attempts = 0
        max_attempts = task.max_retries + 1
        
        while attempts < max_attempts:
            try:
                logger.info(f"Executing task {task.id} ({task.action}). Attempt {attempts + 1}")
                
                # Симуляция вызова плагина
                # В реальной системе здесь будет вызов через TaskRouter и PluginRegistry
                await asyncio.sleep(0.1) 
                
                # Успешное выполнение
                manager.update_task_status(task.id, TaskStatus.SUCCESS, result={"status": "ok"})
                return
                
            except Exception as e:
                attempts += 1
                logger.warning(f"Task {task.id} failed: {e}. Attempts left: {max_attempts - attempts}")
                if attempts >= max_attempts:
                    manager.update_task_status(task.id, TaskStatus.FAILED)
