---
name: daily-sourcing
description: "Runs the prospect finder every weekday morning to source and score new prospects, then prepares audits for the top-ranked ones."
---

# Daily Sourcing Schedule (`daily-sourcing`)

**Cron Expression**: `0 7 * * 1-5` (7:00 AM, Monday–Friday)

---

## Execution Prompt

```
Run the following workflow:
  1. Run /find-prospects with the category and location defined in .agents/rules/icp-definition.md.
  2. Score and rank the results using the combined opportunity and ICP fit score.
  3. For the top 5 prospects only, run /audit to generate their reports, videos, and call scripts.
  4. Save everything to the per-client folders under outputs/clients/.
  5. Do NOT send anything. Do NOT contact anyone.
  6. When finished, write a summary to outputs/daily_brief.md listing:
       - How many prospects were sourced
       - How many audits were generated
       - The top 3 prospects by opportunity score
       - The path to each generated report
```

---

## Operational Constraints

- Hard cap at 5 audits per run. Do not loop.
- If `gmaps-mcp` or LinkedIn MCP returns an error or rate limit, log the event and stop.
- Never invoke any write/mutation tool on LinkedIn or email.
