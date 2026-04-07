---
description: Validate Vast.ai instance end-to-end
---

Run the vastai-validate skill on the currently connected Vast.ai instance.

SSH connection: $ARGUMENTS

Steps:
1. Connect via SSH using the provided connection string
2. Run all validation checks from the vastai-validate skill
3. Report results as a checklist
4. If any check fails, attempt to fix it
5. Re-run failed checks after fix
6. Summarize: what works, what's broken, what needs Docker rebuild
