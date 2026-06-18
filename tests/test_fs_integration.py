import asyncio
import os
import shutil
from pathlib import Path
from loguru import logger
from kernel.planner import ExecutionPlan, TaskNode, ExecutionGraph
from kernel.executor import KernelExecutor
from kernel.state import TaskStatus

async def run_fs_integration_test():
    logger.info("🧪 Starting FS Plugin Integration Test...")
    
    test_dir = Path("temp_test_dir")
    if test_dir.exists():
        shutil.rmtree(test_dir)

    # 1. Формируем план (DAG)
    # Task 1: Создать папку
    # Task 2: Записать файл (зависит от 1)
    # Task 3: Прочитать файл (зависит от 2)
    # Task 4: Листинг папки (зависит от 2)
    
    nodes = [
        TaskNode(id=1, action="fs.mkdir", input={"path": str(test_dir)}),
        TaskNode(id=2, action="fs.write", input={"path": str(test_dir / "test.txt"), "content": "Hello DevOS!"}),
        TaskNode(id=3, action="fs.read", input={"path": str(test_dir / "test.txt")}),
        TaskNode(id=4, action="fs.ls", input={"path": str(test_dir)}),
    ]
    edges = [
        (1, 2),
        (2, 3),
        (2, 4)
    ]
    
    plan = ExecutionPlan(
        intent="Test FS operations in sequence",
        graph=ExecutionGraph(nodes=nodes, edges=edges)
    )
    
    # 2. Инициализируем исполнителя и запускаем план
    executor = KernelExecutor()
    state = await executor.execute_plan(plan)
    
    # 3. Валидация результатов
    logger.info("Verifying execution results...")
    
    assert state.task_statuses[1] == TaskStatus.SUCCESS
    assert state.task_statuses[2] == TaskStatus.SUCCESS
    assert state.task_statuses[3] == TaskStatus.SUCCESS
    assert state.task_statuses[4] == TaskStatus.SUCCESS
    
    # Проверка содержимого из Task 3
    read_result = state.results[3]
    assert read_result["content"] == "Hello DevOS!"
    logger.success(f"Read content correctly: {read_result['content']}")
    
    # Проверка листинга из Task 4
    ls_result = state.results[4]
    assert "test.txt" in ls_result["files"]
    logger.success(f"File found in listing: {ls_result['files']}")

    # Очистка
    if test_dir.exists():
        shutil.rmtree(test_dir)
        
    logger.success("FS Integration Test: PASSED")

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.getcwd())
    asyncio.run(run_fs_integration_test())
