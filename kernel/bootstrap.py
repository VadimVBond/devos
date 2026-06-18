import asyncio
from loguru import logger
from memory.store import init_db

async def bootstrap():
    """Инициализация всех систем DevOS."""
    logger.info("Initializing DevOS Kernel...")
    
    # 1. Инициализация базы данных
    try:
        await init_db()
        logger.success("Memory Layer initialized (SQLite).")
    except Exception as e:
        logger.error(f"Failed to initialize Memory Layer: {e}")
        return False

    # 2. Проверка плагинов (в будущем)
    # 3. Настройка ИИ роутера (в будущем)

    logger.success("DevOS Kernel is ready.")
    return True

if __name__ == "__main__":
    asyncio.run(bootstrap())
