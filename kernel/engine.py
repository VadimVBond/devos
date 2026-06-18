from loguru import logger

from kernel.planner import KernelPlanner
from kernel.executor import KernelExecutor
from kernel.critic import CriticEngine
from plugins.registry import PluginRegistry

class KernelEngine:
    """
    🧠 Главный мозг системы DevOS.
    Pipeline Manager, координирующий Planner -> CriticEngine -> Executor.
    """
    
    def __init__(self, registry: PluginRegistry = None):
        self.registry = registry or PluginRegistry()
        self.planner = KernelPlanner()
        self.critic = CriticEngine(registry=self.registry)
        self.executor = KernelExecutor(registry=self.registry)
        self.is_active = False
        logger.info("DevOS Kernel Engine initialized.")

    async def initialize(self):
        self.is_active = True
        logger.success("DevOS Kernel Engine is now ACTIVE.")
        return True

    async def run_pipeline(self, intent: str):
        """
        Полный цикл выполнения: Интент -> План -> Критик -> Выполнение.
        """
        logger.info(f"--- Pipeline Started for intent: {intent} ---")
        
        # 1. AI Planning
        plan = await self.planner.plan(intent)
        
        # 2. Critic Review
        review = self.critic.review_plan(plan)
        
        if review.status == "rejected":
            logger.error(f"Pipeline ABORTED. Critic rejected the plan. Issues: {review.issues}")
            return {"status": "aborted", "reason": "critic_rejection", "review": review}
            
        # Устанавливаем итоговый граф (может быть модифицирован критиком)
        plan.graph = review.final_graph
        
        # 3. Execution (Assuming observability wrapper is applied externally or here)
        logger.info("Proceeding to execution...")
        result_state = await self.executor.execute_plan(plan)
        
        logger.success("--- Pipeline Finished ---")
        return {"status": "success", "state": result_state, "review": review}
