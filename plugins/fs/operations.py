import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger

class FSHelper:
    """Вспомогательный класс для работы с файловой системой."""

    @staticmethod
    def list_dir(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        abs_path = Path(path).absolute()
        
        if not abs_path.exists():
            raise FileNotFoundError(f"Path {path} does not exist.")
            
        items = os.listdir(abs_path)
        files = [f for f in items if (abs_path / f).is_file()]
        dirs = [d for d in items if (abs_path / d).is_dir()]
        
        return {
            "path": str(abs_path),
            "files": files,
            "directories": dirs,
            "count": len(items)
        }

    @staticmethod
    def read_file(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path")
        if not path:
            raise ValueError("Parameter 'path' is required.")
            
        file_path = Path(path).absolute()
        if not file_path.is_file():
            raise FileNotFoundError(f"File {path} not found.")
            
        content = file_path.read_text(encoding="utf-8")
        return {
            "path": str(file_path),
            "content": content,
            "size": len(content)
        }

    @staticmethod
    def write_file(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path")
        content = params.get("content", "")
        if not path:
            raise ValueError("Parameter 'path' is required.")
            
        file_path = Path(path).absolute()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        
        return {
            "path": str(file_path),
            "status": "written",
            "size": len(content)
        }

    @staticmethod
    def exists(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path")
        if not path:
            raise ValueError("Parameter 'path' is required.")
            
        exists = Path(path).exists()
        return {"path": path, "exists": exists}

    @staticmethod
    def mkdir(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path")
        if not path:
            raise ValueError("Parameter 'path' is required.")
            
        dir_path = Path(path).absolute()
        dir_path.mkdir(parents=True, exist_ok=True)
        return {"path": str(dir_path), "status": "created"}
