from enum import Enum
from typing import Dict, List, Set, Any, Optional
from pydantic import BaseModel, Field
from loguru import logger

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

class ExecutionState(BaseModel):
    """Текущее состояние выполнения графа задач."""
    task_statuses: Dict[int, TaskStatus] = Field(default_factory=dict)
    task_retries: Dict[int, int] = Field(default_factory=dict)
    results: Dict[int, Any] = Field(default_factory=dict)

class ExecutionStateManager:
    """
    Менеджер состояний выполнения. 
    Следит за жизненным циклом задач в DAG.
    """
    
    def __init__(self, nodes: List[Any], edges: List[tuple]):
        self.state = ExecutionState()
        self.nodes = {node.id: node for node in nodes}
        self.edges = edges  # (from_id, to_id)
        
        # Инициализация статусов
        for node_id in self.nodes:
            self.state.task_statuses[node_id] = TaskStatus.PENDING
            self.state.task_retries[node_id] = 0

    def get_ready_tasks(self) -> List[int]:
        """Возвращает ID задач, чьи зависимости выполнены."""
        ready = []
        for node_id, status in self.state.task_statuses.items():
            if status != TaskStatus.PENDING:
                continue
            
            # Ищем зависимости (входящие ребра)
            dependencies = [src for src, dst in self.edges if dst == node_id]
            
            if all(self.state.task_statuses.get(dep) == TaskStatus.SUCCESS for dep in dependencies):
                ready.append(node_id)
            elif any(self.state.task_statuses.get(dep) == TaskStatus.FAILED for dep in dependencies):
                # Если хоть один родитель упал, помечаем как SKIPPED
                self.update_task_status(node_id, TaskStatus.SKIPPED)
                
        return ready

    def update_task_status(self, task_id: int, status: TaskStatus, result: Any = None):
        """Обновляет статус задачи и обрабатывает каскадные изменения."""
        self.state.task_statuses[task_id] = status
        if result is not None:
            self.state.results[task_id] = result
        
        logger.info(f"Task {task_id} status updated to: {status}")
        
        # Каскадный пропуск при провале
        if status == TaskStatus.FAILED or status == TaskStatus.SKIPPED:
            self._skip_descendants(task_id)

    def _skip_descendants(self, task_id: int):
        """Рекурсивно помечает всех потомков как SKIPPED."""
        descendants = [dst for src, dst in self.edges if src == task_id]
        for desc_id in descendants:
            if self.state.task_statuses[desc_id] == TaskStatus.PENDING:
                self.update_task_status(desc_id, TaskStatus.SKIPPED)
