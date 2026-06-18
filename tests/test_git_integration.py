import asyncio
import os
import shutil
from pathlib import Path
from loguru import logger
from kernel.planner import ExecutionPlan, TaskNode, ExecutionGraph
from kernel.executor import KernelExecutor
from kernel.state import TaskStatus
from plugins.git.operations import GitHelper

async def run_git_integration_test():
    logger.info("🧪 Starting Git Plugin Integration Test...")
    
    test_dir = Path("temp_git_test")
    
    def cleanup():
        if test_dir.exists():
            GitHelper.fix_git_permissions(str(test_dir))
            shutil.rmtree(test_dir)

    cleanup()
    test_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Формируем план (DAG)
        nodes = [
            TaskNode(id=1, action="git.init", input={"path": str(test_dir)}),
            TaskNode(id=2, action="fs.write", input={"path": str(test_dir / "README.md"), "content": "# Test Repo"}),
            TaskNode(id=3, action="git.add", input={"path": str(test_dir), "files": ["README.md"]}),
            TaskNode(id=4, action="git.commit", input={"path": str(test_dir), "message": "Initial commit"}),
            TaskNode(id=5, action="git.status", input={"path": str(test_dir)}),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5)
        ]
        
        plan = ExecutionPlan(
            intent="Initialize git and make first commit",
            graph=ExecutionGraph(nodes=nodes, edges=edges)
        )
        
        # 2. Исполнение
        executor = KernelExecutor()
        state = await executor.execute_plan(plan)
        
        # 3. Валидация
        logger.info("Verifying git execution results...")
        assert state.task_statuses[1] == TaskStatus.SUCCESS
        assert state.task_statuses[4] == TaskStatus.SUCCESS
        
        # Проверка существования .git
        assert (test_dir / ".git").exists()
        logger.success("Git repository initialized and commit created successfully.")
        
    finally:
        cleanup()
        
    logger.success("Git Integration Test: PASSED")

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.getcwd())
    asyncio.run(run_git_integration_test())
