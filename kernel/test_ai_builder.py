import asyncio
from loguru import logger
from kernel.planner import KernelPlanner
from ai.runtime import AIRuntime

async def test_ai_graph_builder():
    logger.info("🧪 Testing AI Graph Builder Layer...")
    
    runtime = AIRuntime()
    planner = KernelPlanner(runtime=runtime)
    
    # Тест 1: Успешная генерация (симуляция)
    intent = "Scan repository and analyze code"
    logger.info(f"Test 1: Valid intent -> {intent}")
    plan = await planner.plan(intent)
    
    assert plan.intent == intent
    assert len(plan.graph.nodes) == 2
    assert len(plan.graph.edges) == 1
    logger.success("Test 1: PASSED (Valid DAG generated)")

    # Тест 2: Валидация цикла (ожидаем ошибку)
    logger.info("Test 2: Cycle detection...")
    invalid_raw = {
        "intent": "cycle test",
        "graph": {
            "nodes": [{"id": 1, "action": "a"}, {"id": 2, "action": "b"}],
            "edges": [[1, 2], [2, 1]]
        }
    }
    
    try:
        from kernel.planner import ExecutionPlan
        ExecutionPlan(**invalid_raw)
        logger.error("Test 2: FAILED (Cycle not detected)")
    except ValueError as e:
        logger.success(f"Test 2: PASSED (Cycle detected: {e})")

    # Тест 3: Несуществующий узел (ожидаем ошибку)
    logger.info("Test 3: Missing node ID detection...")
    invalid_raw_nodes = {
        "intent": "missing node test",
        "graph": {
            "nodes": [{"id": 1, "action": "a"}],
            "edges": [[1, 99]]
        }
    }
    try:
        ExecutionPlan(**invalid_raw_nodes)
        logger.error("Test 3: FAILED (Missing node ID not detected)")
    except ValueError as e:
        logger.success(f"Test 3: PASSED (Missing node ID detected: {e})")

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())
    asyncio.run(test_ai_graph_builder())
