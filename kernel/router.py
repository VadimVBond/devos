from loguru import logger

class TaskRouter:
    """Маршрутизатор задач между ядром и плагинами."""
    
    def __init__(self):
        self.is_ready = True
        logger.info("Task Router initialized.")

    def route(self, action: str):
        logger.debug(f"Routing action: {action}")
        return f"plugin_for_{action}"
