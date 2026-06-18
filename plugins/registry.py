from typing import Dict, Any, List, Callable
from pydantic import BaseModel
from loguru import logger
from plugins.fs.operations import FSHelper
from plugins.git.operations import GitHelper

class PluginSchema(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    func: Callable[[Dict[str, Any]], Dict[str, Any]]

class PluginRegistry:
    """Реестр и загрузчик плагинов."""
    
    def __init__(self):
        self.plugins: Dict[str, PluginSchema] = {}
        self._register_fs_plugins()
        self._register_git_plugins()
        logger.info(f"Plugin Registry initialized with {len(self.plugins)} plugins.")

    def _register_fs_plugins(self):
        """Регистрация плагинов для работы с файловой системой."""
        fs_actions = [
            {"name": "fs.ls", "desc": "Листинг директории", "input": {"path": "string"}, "output": {"files": "list", "directories": "list"}, "func": FSHelper.list_dir},
            {"name": "fs.read", "desc": "Чтение файла", "input": {"path": "string"}, "output": {"content": "string"}, "func": FSHelper.read_file},
            {"name": "fs.write", "desc": "Запись в файл", "input": {"path": "string", "content": "string"}, "output": {"status": "string"}, "func": FSHelper.write_file},
            {"name": "fs.exists", "desc": "Проверка существования пути", "input": {"path": "string"}, "output": {"exists": "boolean"}, "func": FSHelper.exists},
            {"name": "fs.mkdir", "desc": "Создание директории", "input": {"path": "string"}, "output": {"status": "string"}, "func": FSHelper.mkdir}
        ]
        self._batch_register(fs_actions)

    def _register_git_plugins(self):
        """Регистрация плагинов для работы с Git."""
        git_actions = [
            {"name": "git.init", "desc": "Инициализация репозитория", "input": {"path": "string"}, "output": {"status": "string"}, "func": GitHelper.init},
            {"name": "git.add", "desc": "Добавление файлов в индекс", "input": {"path": "string", "files": "list"}, "output": {"status": "string"}, "func": GitHelper.add},
            {"name": "git.commit", "desc": "Создание коммита", "input": {"path": "string", "message": "string"}, "output": {"status": "string"}, "func": GitHelper.commit},
            {"name": "git.status", "desc": "Статус репозитория", "input": {"path": "string"}, "output": {"status_output": "string"}, "func": GitHelper.status},
            {"name": "git.branch", "desc": "Управление ветками", "input": {"path": "string", "name": "string", "create": "boolean"}, "output": {"branch": "string"}, "func": GitHelper.branch}
        ]
        self._batch_register(git_actions)

    def _batch_register(self, actions: List[Dict[str, Any]]):
        for action in actions:
            schema = PluginSchema(
                name=action["name"],
                description=action["desc"],
                input_schema=action["input"],
                output_schema=action["output"],
                func=action["func"]
            )
            self.plugins[schema.name] = schema

    def list_plugins(self) -> List[str]:
        return list(self.plugins.keys())

    def get_plugin(self, name: str) -> PluginSchema:
        return self.plugins.get(name)

    def execute(self, name: str, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполняет действие плагина."""
        plugin = self.get_plugin(name)
        if not plugin:
            raise ValueError(f"Plugin action '{name}' not found.")
        
        logger.debug(f"Executing plugin action: {name} with params: {params}, context: {context}")
        return plugin.func(params)
