import subprocess
import os
import stat
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger

class GitHelper:
    """Вспомогательный класс для работы с Git через subprocess."""

    @staticmethod
    def _run_git(args: List[str], cwd: Optional[str] = None) -> str:
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e.cmd} | Error: {e.stderr}")
            raise RuntimeError(f"Git error: {e.stderr.strip()}")

    @staticmethod
    def init(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        abs_path = Path(path).absolute()
        abs_path.mkdir(parents=True, exist_ok=True)
        
        output = GitHelper._run_git(["init"], cwd=str(abs_path))
        return {"path": str(abs_path), "output": output, "status": "initialized"}

    @staticmethod
    def add(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        files = params.get("files", ["."])
        if isinstance(files, str):
            files = [files]
            
        abs_path = Path(path).absolute()
        GitHelper._run_git(["add"] + files, cwd=str(abs_path))
        return {"path": str(abs_path), "added_files": files, "status": "added"}

    @staticmethod
    def commit(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        message = params.get("message")
        if not message:
            raise ValueError("Commit message is required.")
            
        abs_path = Path(path).absolute()
        output = GitHelper._run_git(["commit", "-m", message], cwd=str(abs_path))
        return {"path": str(abs_path), "output": output, "status": "committed"}

    @staticmethod
    def status(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        abs_path = Path(path).absolute()
        output = GitHelper._run_git(["status", "--porcelain"], cwd=str(abs_path))
        return {"path": str(abs_path), "status_output": output}

    @staticmethod
    def branch(params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        name = params.get("name")
        create = params.get("create", True)
        
        abs_path = Path(path).absolute()
        args = ["checkout", "-b", name] if create else ["checkout", name]
        output = GitHelper._run_git(args, cwd=str(abs_path))
        return {"path": str(abs_path), "branch": name, "output": output}

    @staticmethod
    def fix_git_permissions(path: str):
        """Рекурсивно меняет права доступа в папке .git для возможности удаления в Windows."""
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IWRITE)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IWRITE)
