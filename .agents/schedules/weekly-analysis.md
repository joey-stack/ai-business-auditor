---
name: weekly-analysis
description: "Runs the outreach outcome analysis every Friday afternoon and updates the outreach templates based on what's working."
---

# Weekly Outcome Analysis Schedule (`weekly-analysis`)

**Cron Expression**: `0 16 * * 5` (4:00 PM, Friday)

---

## Execution Prompt

```
1. Run /outcome-analysis across all logged touches in outputs/outreach_outcomes.csv and outputs/clients/*/outreach_log.csv.
2. Identify which opening lines, subject lines, and objection responses produced the highest reply rates.
3. Update the outreach sequence copy and call scripts with the top-performing patterns.
4. Write the insights to outputs/insights/outreach_insights.md.
5. Do NOT send anything. Do NOT contact anyone.
```

---

## Operational Boundaries

- Purely analytical and template refinement run.
- Zero outbound messaging.
