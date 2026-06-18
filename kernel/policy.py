from loguru import logger

class PolicyGuard:
    """Слой безопасности и политик выполнения."""
    
    def __init__(self):
        self.forbidden_keywords = ["delete", "remove", "format"]
        logger.info("Policy Guard initialized.")

    def validate(self, intent: str) -> bool:
        """Проверка интента на безопасность."""
        for word in self.forbidden_keywords:
            if word in intent.lower():
                logger.warning(f"Policy violation: forbidden word '{word}' found in intent.")
                return False
        return True
