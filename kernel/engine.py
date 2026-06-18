from loguru import logger

from kernel.planner import KernelPlanner
from kernel.executor import KernelExecutor
from kernel.critic import CriticEngine
from plugins.registry import PluginRegistry
from kernel.feedback import (
    KnowledgeBase, FeedbackAnalyzer, FilterLayer, ContextBuilder
)

class KernelEngine:
    """
    🧠 Главный мозг системы DevOS.
    Pipeline Manager, координирующий Planner -> CriticEngine -> Executor -> Feedback.
    """
    
    def __init__(self, registry: PluginRegistry = None):
        self.registry = registry or PluginRegistry()
        self.planner = KernelPlanner()
        self.critic = CriticEngine(registry=self.registry)
        self.executor = KernelExecutor(registry=self.registry)
        
        # Feedback Layer Initialization
        self.kb = KnowledgeBase()
        self.feedback_analyzer = FeedbackAnalyzer(self.kb)
        self.feedback_filter = FilterLayer()
        self.context_builder = ContextBuilder()
        
        self.is_active = False
        logger.info("DevOS Kernel Engine initialized.")

    async def initialize(self):
        self.is_active = True
        logger.success("DevOS Kernel Engine is now ACTIVE.")
        return True

    async def run_pipeline(self, intent: str):
        """
        Полный цикл выполнения: Интент -> План -> Критик -> Выполнение -> Анализ.
        """
        logger.info(f"--- Pipeline Started for intent: {intent} ---")
        
        # 0. Build Feedback Context
        patterns = self.kb.get_all_patterns()
        filtered_patterns = self.feedback_filter.filter(patterns)
        feedback_context = self.context_builder.build_context(filtered_patterns)
        
        # 1. AI Planning
        plan = await self.planner.plan(intent, feedback_context=feedback_context)
        
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
        
        # 4. Feedback Analysis (We extract dummy traces for example, but realistically it's from observability)
        # Assuming we can parse the execution state to find failed tasks:
        # result_state contains task_statuses.
        from kernel.state import TaskStatus
        events_for_feedback = []
        for task_id, status in result_state.task_statuses.items():
            node = next((n for n in plan.graph.nodes if n.id == task_id), None)
            if node and status == TaskStatus.FAILED:
                events_for_feedback.append({
                    "event_type": "TaskFailed",
                    "action": node.action,
                    "error": "Failed during execution state evaluation."
                })
        
        if events_for_feedback:
            self.feedback_analyzer.analyze_execution_state(
                state=result_state.model_dump(),
                graph_events=events_for_feedback
            )
        
        logger.success("--- Pipeline Finished ---")
        return {"status": "success", "state": result_state, "review": review}
