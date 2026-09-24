---
name: daily-batch-pursuit
description: "Runs the top-N pursuit workflow every weekday morning to source, score, audit, and prepare ready-to-dispatch client packages."
---

# Daily Batch Pursuit Schedule (`daily-batch-pursuit`)

**Cron Expression**: `0 7 * * 1-5` (7:00 AM UTC/Local, Monday through Friday)

---

## Execution Prompt

```
Run /pursue-top-prospects --count 20 with the category and location specified in .agents/rules/icp-definition.md.

When finished, compile the daily brief to outputs/daily_brief.md and STOP.
Do NOT send anything. Do NOT contact anyone.
```

---

## Operational Boundaries

1. **Autonomous Deliverable Preparation Only**:
   - Executes research, enrichment, four-pillar diagnostics, report verification, PDF compilation, and call script generation.
   - Saves all artifacts into `outputs/clients/<company-slug>/`.
2. **Zero Human Contact**:
   - Never calls phone lines, never triggers emails, and never invokes LinkedIn write tools (`send_message`, `connect_with_person`).
3. **Graceful Throttling**:
   - Caps batch execution strictly at 20 prospects.
   - If rate limits occur on enrichment or maps scrapers, logs the incident and exits cleanly.
