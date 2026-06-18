import asyncio
import json
from loguru import logger
from kernel.planner import ExecutionPlan, TaskNode, ExecutionGraph
from kernel.executor import KernelExecutor
from kernel.state import TaskStatus

async def test_dag_execution():
    logger.info("🧪 Testing Execution Graph (DAG) Layer...")
    
    # 1. Создаем тестовый граф:
    # Task 1 (Root)
    # Task 2 (Depends on 1)
    # Task 3 (Depends on 1)
    # Task 4 (Depends on 2 and 3)
    
    nodes = [
        TaskNode(id=1, action="fs.list", max_retries=1),
        TaskNode(id=2, action="fs.read", max_retries=0),
        TaskNode(id=3, action="ai.analyze", max_retries=2),
        TaskNode(id=4, action="git.commit", max_retries=0),
    ]
    edges = [
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 4)
    ]
    
    plan = ExecutionPlan(
        intent="Scan, analyze and commit",
        graph=ExecutionGraph(nodes=nodes, edges=edges)
    )
    
    # 2. Запускаем выполнение
    executor = KernelExecutor()
    final_state = await executor.execute_plan(plan)
    
    # 3. Проверяем результаты
    logger.info("Verification of results:")
    for tid, status in final_state.task_statuses.items():
        logger.info(f"Task {tid}: {status}")
        
    all_success = all(s == TaskStatus.SUCCESS for s in final_state.task_statuses.values())
    if all_success:
        logger.success("DAG Execution Test: PASSED")
    else:
        logger.error("DAG Execution Test: FAILED")

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())
    asyncio.run(test_dag_execution())
