import asyncio
import json
from loguru import logger

# Импорты компонентов
from kernel.engine import KernelEngine
from kernel.router import TaskRouter
from kernel.policy import PolicyGuard
from kernel.planner import KernelPlanner
from plugins.registry import PluginRegistry
from memory.store import create_session, store_kv

async def run_boot_test():
    logger.info("🚀 Starting DevOS Bootstrap Validation Mode...")
    
    results = {
        "boot_status": "FAIL",
        "failed_checks": [],
        "warnings": [],
        "system_summary": ""
    }
    
    try:
        # CHECK 1: Kernel Load
        engine = KernelEngine()
        await engine.initialize()
        router = TaskRouter()
        if not (engine.is_active and router.is_ready):
            results["failed_checks"].append("Kernel Load")
        
        # CHECK 2: Plugin Registry
        registry = PluginRegistry()
        plugins = registry.list_plugins()
        if not plugins:
            results["failed_checks"].append("Plugin Registry (empty)")
        for p_name in plugins:
            p = registry.get_plugin(p_name)
            if not (p.name and p.input_schema and p.output_schema):
                results["failed_checks"].append(f"Plugin Schema: {p_name}")

        # CHECK 3: Memory Layer
        await create_session("boot_test")
        await store_kv("status", "ok")

        # CHECK 4: Execution Pipeline Test
        planner = KernelPlanner()
        intent = "analyze current project structure"
        plan = await planner.plan(intent)
        if plan.intent != intent:
            results["failed_checks"].append("Execution Pipeline (Intent mismatch)")

        # CHECK 5: Safety Policy
        policy = PolicyGuard()
        unsafe_intent = "delete all files"
        if policy.validate(unsafe_intent) is not True:
            logger.success("Policy Guard correctly blocked unsafe command.")
        else:
            results["failed_checks"].append("Safety Policy (Bypass detected)")

        # Final Evaluation
        if not results["failed_checks"]:
            results["boot_status"] = "PASS"
            results["system_summary"] = "All core systems initialized and validated successfully."
        else:
            results["system_summary"] = f"Validation failed in: {', '.join(results['failed_checks'])}"

    except Exception as e:
        logger.exception("Unexpected error during boot test")
        results["failed_checks"].append(f"Runtime Error: {str(e)}")
        results["system_summary"] = "System crash during bootstrap."

    print("\n--- FINAL BOOT TEST RESULT ---")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("------------------------------\n")

if __name__ == "__main__":
    # Установка PYTHONPATH для корректных импортов при запуске напрямую
    import os
    import sys
    sys.path.append(os.getcwd())
    
    asyncio.run(run_boot_test())
