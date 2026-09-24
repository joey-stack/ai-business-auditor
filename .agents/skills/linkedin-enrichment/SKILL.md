---
name: linkedin-enrichment
description: "Resolves prospect decision-maker profiles, extracts recent posts, analyzes activity for pain signals, and generates tailored approach strategies. READ-ONLY: never sends messages or connection requests."
---

# LinkedIn Enrichment Skill (`linkedin-enrichment`)

This skill enriches verified business prospects with decision-maker identity, analyzes their recent LinkedIn publications and activity for operational pain points, and synthesizes a high-conversion, non-invasive outreach approach strategy.

---

## 1. Purpose

Identify the key decision-maker (Owner, CEO, Managing Director, Operations Director) at a target company, review their public posts and activity to understand their immediate business priorities and frustrations, and produce a contextual approach strategy.

---

## 2. Input Specification

- **`company_name`** (`string`, required): Name of the business.
- **`domain`** (`string`, optional): Business website domain.
- **`target_roles`** (`string[]`, optional): Preferred job titles (defaults to `["Owner", "Founder", "CEO", "Managing Director", "Operations Director", "General Manager"]`).
- **`read_activity`** (`boolean`, optional): Whether to fetch and analyze recent posts (default: `true`).
- **`max_posts`** (`number`, optional): Maximum number of recent posts to inspect (default: `10`, capped at `10`).

---

## 3. Step-by-Step Execution Process

### Step 1: Decision-Maker Search
1. Query `search_people` with keywords combining company and leadership titles:
   ```
   "{company_name} {target_role}"
   ```
2. Identify the highest-ranking executive actively verified at the company.
3. If no executive profile is located, return `{"found": false}` and stop.

### Step 2: Profile Retrieval
1. Call `get_person_profile` using the resolved person's identifier.
2. If `read_activity` is `true`, include `sections=["posts"]` to retrieve up to `max_posts` recent posts.
3. Extract verified profile fields:
   - Full Name
   - Primary Headline
   - Current Title & Organization
   - Geographic Location
   - Public LinkedIn URL

### Step 3: Activity & Sentiment Analysis
Analyze the returned posts across five diagnostic dimensions:
1. **Posting Frequency & Recency**: Is this person an active publisher (posted in last 14 days), an occasional contributor, or dormant?
2. **Communication Tone**: Executive, technical, community-oriented, celebratory, or venting/candid.
3. **Operational Pain Signals**: Explicit or implicit friction mentioned in posts (e.g., staffing shortages, software complexity, manual quoting delays, client communication lag, invoice disputes).
4. **Recurring Themes**: Topics the prospect frequently addresses (e.g., quality craftsmanship, customer experience, team training, scaling pains).
5. **Conversation Hooks**: Specific, relevant public statements, completed projects, or questions posed to their audience that can serve as natural conversation starters.

### Step 4: Approach Strategy Generation
Synthesize an `approach_strategy` tailored to the prospect:
- **`opening_line`**: A respectful, personalized icebreaker referencing a public topic or project they highlighted (never creepy, invasive, or sounding automated).
- **`channel_recommendation`**: Best contact method (`"email"`, `"phone"`, or `"linkedin"`) aligned with their communication style and outreach compliance rules.
- **`timing_note`**: Optimal time of day or week to initiate contact based on their activity patterns.
- **`topics_to_avoid`**: Sensitive, political, controversial, or personal matters identified in posts.
- **`reasoning`**: The strategic rationale connecting their visible priorities with our consulting/audit solutions.

---

## 4. Output JSON Schema

```json
{
  "company_name": string,
  "decision_maker": {
    "found": boolean,
    "name": string | null,
    "title": string | null,
    "headline": string | null,
    "profile_url": string | null,
    "recent_activity": {
      "posts_analyzed": number,
      "last_post_date": string | null,
      "tone": string | null,
      "pain_signals": string[],
      "recurring_themes": string[],
      "conversation_hooks": string[]
    },
    "approach_strategy": {
      "opening_line": string,
      "channel_recommendation": "email" | "phone" | "linkedin",
      "timing_note": string,
      "topics_to_avoid": string[],
      "reasoning": string
    }
  }
}
```

---

## 5. Hard Constraints & Safety Governance

1. **Strict READ-ONLY Enforcement**:
   - **Never call `connect_with_person`, `send_message`, `send_inmail`, or any write/mutation tool**.
   - The AI only gathers intelligence and drafts strategy. The human consultant sends all outreach manually.
2. **Quota & Rate-Limit Protections**:
   - Maximum **5 LinkedIn tool calls per prospect**.
   - Maximum **5 prospects enriched per run/batch**.
3. **Session & Checkpoint Handling**:
   - LinkedIn session data persists in `~/.linkedin-mcp/profile`.
   - On first run, a real browser window opens to allow the human operator to log in once.
   - If a CAPTCHA, verification code, or account checkpoint appears, **stop immediately** and alert the human operator. Never attempt automated evasion.
4. **Ethical Communication Standards**:
   - Never quote personal or family-related posts.
   - Do not claim familiarity or fabricate prior interaction.
   - Keep outreach references strictly focused on publicly shared business or industry topics.
