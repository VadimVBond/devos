import asyncio
from typing import Dict, Any, List
from loguru import logger
from kernel.state import ExecutionStateManager, TaskStatus
from kernel.planner import ExecutionPlan, TaskNode
from plugins.registry import PluginRegistry

class KernelExecutor:
    """
    Исполнитель графа задач (Graph-Aware Executor).
    Управляет запуском задач с учетом зависимостей и повторных попыток.
    """
    
    def __init__(self, registry: PluginRegistry = None):
        self.registry = registry or PluginRegistry()
        logger.info("Kernel Executor initialized with Plugin Registry.")

    async def execute_plan(self, plan: ExecutionPlan):
        """Выполняет обычный неоптимизированный план, обходя DAG."""
        # Этот метод оставлен для обратной совместимости, если не используется Optimizer
        manager = ExecutionStateManager(
            nodes=plan.graph.nodes, 
            edges=plan.graph.edges
        )
        
        logger.info(f"Starting execution for intent: {plan.intent}")
        
        while True:
            ready_task_ids = manager.get_ready_tasks()
            
            if not ready_task_ids:
                pending_tasks = [tid for tid, status in manager.state.task_statuses.items() 
                                if status == TaskStatus.PENDING]
                if not pending_tasks:
                    break
                else:
                    break

            # Запускаем готовые задачи
            for task_id in ready_task_ids:
                task_node = manager.nodes[task_id]
                await self._run_task(task_node, manager)

        logger.success("Execution graph processing finished.")
        return manager.state

    async def execute_optimized_graph(self, opt_graph):
        """
        Выполняет граф пакетами (batches), гарантируя детерминизм и безопасность 
        через execute_batch (где используется asyncio.gather).
        """
        manager = ExecutionStateManager(
            nodes=opt_graph.optimized_graph.nodes, 
            edges=opt_graph.optimized_graph.edges
        )
        
        logger.info("Starting optimized batch execution.")
        
        for batch_index, batch_task_ids in enumerate(opt_graph.execution_batches):
            logger.info(f"Executing Batch {batch_index} with {len(batch_task_ids)} tasks.")
            
            # Собираем список нод для батча
            batch_nodes = []
            for tid in batch_task_ids:
                node = manager.nodes.get(tid)
                if node:
                    batch_nodes.append(node)
                    
            if batch_nodes:
                await self.execute_batch(batch_nodes, manager)
                
            # Проверяем, не упала ли какая-то задача в батче, если да - возможно нужно прервать
            failed_tasks = [tid for tid in batch_task_ids if manager.state.task_statuses.get(tid) == TaskStatus.FAILED]
            if failed_tasks:
                logger.error(f"Batch {batch_index} failed on tasks: {failed_tasks}. Aborting execution.")
                break

        logger.success("Optimized execution graph processing finished.")
        return manager.state

    async def execute_batch(self, batch_nodes: List[TaskNode], manager: ExecutionStateManager):
        """
        Выполняет группу полностью независимых задач конкурентно.
        """
        tasks = [self._run_task(node, manager) for node in batch_nodes]
        await asyncio.gather(*tasks)

    async def _run_task(self, task: TaskNode, manager: ExecutionStateManager):
        """Выполняет конкретную задачу с учетом Retry Policy."""
        manager.update_task_status(task.id, TaskStatus.RUNNING)
        
        attempts = 0
        max_attempts = task.max_retries + 1
        
        while attempts < max_attempts:
            try:
                logger.info(f"Executing task {task.id} ({task.action}). Attempt {attempts + 1}")
                
                # Реальный вызов плагина с передачей контекста выполнения
                result = self.registry.execute(
                    task.action, 
                    task.input, 
                    context={"task_id": task.id}
                )
                
                # Успешное выполнение
                manager.update_task_status(task.id, TaskStatus.SUCCESS, result=result)
                return
                
            except Exception as e:
                attempts += 1
                logger.warning(f"Task {task.id} failed: {e}. Attempts left: {max_attempts - attempts}")
                if attempts >= max_attempts:
                    manager.update_task_status(task.id, TaskStatus.FAILED)
