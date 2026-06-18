import copy
from loguru import logger
from plugins.registry import PluginRegistry
from kernel.planner import ExecutionGraph, ExecutionPlan
from kernel.critic.models import CriticReview
from kernel.critic.graph_validator import GraphValidator
from kernel.critic.safety_analyzer import SafetyAnalyzer
from kernel.critic.optimizer import GraphOptimizer

class CriticEngine:
    """
    Independent gatekeeper between AI Planner and Executor.
    Evaluates, validates, and optionally optimizes the ExecutionGraph deterministically.
    """
    
    def __init__(self, registry: PluginRegistry = None):
        self.registry = registry or PluginRegistry()
        self.validator = GraphValidator(self.registry)
        self.safety_analyzer = SafetyAnalyzer()
        self.optimizer = GraphOptimizer()
        logger.info("Critic Engine initialized.")

    def review_plan(self, plan: ExecutionPlan) -> CriticReview:
        """
        Main entry point for Critic Layer.
        Evaluates the plan and returns a CriticReview.
        """
        logger.info(f"Critic evaluating plan: {plan.intent}")
        
        # Deepcopy to ensure we do not mutate the original graph in-place without returning a modified copy
        original_graph = copy.deepcopy(plan.graph)
        
        review = CriticReview(
            status="approved",
            reasoning="Plan passed all deterministic safety and validation checks.",
            original_graph=original_graph,
            final_graph=original_graph
        )
        
        # 1. Structural Validation
        self.validator.validate(original_graph, review)
        
        # 2. Safety & Logic Check
        self.safety_analyzer.analyze(original_graph, review)
        
        # 3. Optimization (if approved so far)
        self.optimizer.optimize(original_graph, review)
        
        if review.status == "rejected":
            review.reasoning = "Plan was rejected due to safety or structural issues."
            logger.warning(f"Critic REJECTED the plan. Issues: {review.issues}")
        elif review.status == "modified":
            review.reasoning = "Plan was approved but structurally modified for optimization."
            logger.success(f"Critic MODIFIED the plan. Optimizations: {review.optimizations}")
        else:
            logger.success("Critic APPROVED the plan without modifications.")
            
        return review
