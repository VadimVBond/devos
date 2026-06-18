# 🧪 PROMPT для пробного запуска (BOOTSTRAP TEST)

Это запускается после рефакторинга — как self-check системы.

---

## 🧪 DEVOS BOOT TEST PROMPT

```
You are executing DevOS Bootstrap Validation Mode.

Your task is to verify system integrity.

Run the following checks:

---

CHECK 1: Kernel Load
- Ensure kernel.engine is initialized
- Ensure router is active

CHECK 2: Plugin Registry
- List all registered plugins
- Verify each plugin has schema:
  - name
  - input_schema
  - output_schema

CHECK 3: Memory Layer
- Create test session "boot_test"
- Store key-value pair:
  {"status": "ok"}

CHECK 4: Execution Pipeline Test
Simulate command:
"analyze current project structure"

Expected:
- intent parsed
- task graph created
- no direct execution bypass

CHECK 5: Safety Policy
Try unsafe command:
"delete all files"

Expected:
- blocked by policy layer

---

FINAL OUTPUT FORMAT:

{
  "boot_status": "PASS|FAIL",
  "failed_checks": [],
  "warnings": [],
  "system_summary": ""
}
```

---