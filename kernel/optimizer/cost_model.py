from typing import Dict

class CostModel:
    """
    Модель стоимости операций для принятия решений при оптимизации.
    Оценивает нагрузку на ресурсы (CPU, сеть, диск, время).
    """
    
    BASE_COSTS: Dict[str, float] = {
        "fs.ls": 1.0,
        "fs.exists": 1.0,
        "fs.read": 2.0,
        "fs.mkdir": 3.0,
        "fs.write": 5.0,
        "git.status": 5.0,
        "git.branch": 10.0,
        "git.add": 15.0,
        "git.commit": 20.0,
        "git.init": 30.0,
        "system.shell": 50.0
    }
    
    DEFAULT_COST = 20.0

    @classmethod
    def get_action_cost(cls, action: str) -> float:
        return cls.BASE_COSTS.get(action, cls.DEFAULT_COST)
