from typing import Dict, Any, List
from pydantic import BaseModel
from loguru import logger

class PluginSchema(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]

class PluginRegistry:
    """Реестр и загрузчик плагинов."""
    
    def __init__(self):
        self.plugins: Dict[str, PluginSchema] = {}
        self._register_defaults()
        logger.info(f"Plugin Registry initialized with {len(self.plugins)} plugins.")

    def _register_defaults(self):
        # Регистрация тестового FS плагина
        fs_plugin = PluginSchema(
            name="fs.analyze",
            description="Анализ структуры файловой системы",
            input_schema={"path": "string"},
            output_schema={"files": "list", "directories": "list"}
        )
        self.plugins[fs_plugin.name] = fs_plugin

    def list_plugins(self) -> List[str]:
        return list(self.plugins.keys())

    def get_plugin(self, name: str) -> PluginSchema:
        return self.plugins.get(name)
