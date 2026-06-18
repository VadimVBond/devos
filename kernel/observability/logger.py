import os
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from kernel.observability.events import BaseEvent
from loguru import logger

class AsyncEventLogger:
    """Асинхронный логгер для записи событий в JSON."""
    
    def __init__(self, log_dir: str = ".runtime/logs/traces"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._buffer: List[BaseEvent] = []
        self._lock = asyncio.Lock()
        
    async def log_event(self, event: BaseEvent):
        """Добавляет событие в буфер. В реальной системе тут может быть сброс по таймеру или размеру."""
        async with self._lock:
            self._buffer.append(event)
            logger.debug(f"Event logged: {event.event_type} [{event.event_id}]")
            
    async def flush(self, graph_id: str):
        """Сбрасывает буфер в файл для конкретного выполнения."""
        async with self._lock:
            if not self._buffer:
                return
                
            file_path = self.log_dir / f"{graph_id}.json"
            
            # Собираем данные
            data = [event.model_dump() for event in self._buffer]
            
            # Пишем на диск
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.success(f"Execution trace saved to {file_path}")
            self._buffer.clear()
