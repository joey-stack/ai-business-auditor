---
name: call-script
description: "Generates a branching phone call script for a specific prospect based on their audit findings, covering the opening, common objections, expected questions, and closing paths. Use before calling a prospect who has received or been offered an audit report."
---

# Call Script Generation Skill (`call-script`)

This skill generates a personalized, branching phone call decision tree tailored to a specific business prospect based on their verified audit findings, digital presence tier, and LinkedIn approach strategy.

---

## 1. Purpose

Produce a practical, spoken-word call script tailored to **ONE** prospect, equipping the consultant with prepared branches for likely objections, questions, and closing opportunities without resorting to pressure tactics.

---

## 2. Input Specification

- **`prospect_name`** (`string`, required): Name of the business or decision-maker.
- **`audit_json`** (`object`, required): The completed audit findings and scoring record for this prospect.
- **`approach_strategy`** (`object`, optional): The approach strategy derived from LinkedIn post and activity analysis (opening line, preferred channel, timing, topics to avoid).
- **`presence_tier`** (`"A" | "B" | "C" | "D"`, optional): Digital presence tier established during prospecting or audit.

---

## 3. Step-by-Step Execution Process

1. **Extract Core Talking Points**:
   - Inspect `audit_json` and isolate the **3 most significant operational findings or friction points** (e.g., missing website, broken mobile booking flow, unanswered customer inquiries, slow response latency).
   - Reframe each finding as an **objective observation**, never a criticism or attack.

2. **Diagnose Prospect Perspective & Primary Concern**:
   - Evaluate the prospect's profile:
     - **Tier D / Local Trades**: May be unfamiliar with technical jargon (SEO, CTR, GBP) and prioritize simple job booking and phone inquiries.
     - **Tier A / High-Scale Corporate**: May have internal IT teams, prior agency fatigue, or skepticism regarding external claims.

3. **Construct the Branching Decision Tree**:
   Assemble the script into structured sections:

   - **Section A — Opening (0:00–0:30)**:
     - Exact conversational greeting when they answer.
     - Permission-based opener: *"Do you have 60 seconds?"*
     - Clear, personalized reason for the call directly relevant to their business.

   - **Section B — The Hook (0:30–1:30)**:
     - Objective citation of finding #1 from the audit.
     - One-sentence statement of real-world business consequence (*"what this usually means is..."*).

   - **Section C — The Branch Point (1:30–2:00)**:
     - The pivot question that splits the dialogue:
       *"Would it be useful if I sent you the 2-page breakdown?"* OR *"Is that an area you've been looking at recently?"*
     - Map 3 distinct prospect reactions into corresponding branches (Engaged / Skeptical / Neutral).

   - **Section D — The 10 Objection Branches**:
     Provide prepared, non-defensive responses for each of the following 10 scenarios:
     1. *"I'm too busy right now."*
     2. *"I don't have the budget."*
     3. *"I already have someone doing this."*
     4. *"I tried SEO/marketing before and it didn't work."*
     5. *"I need to think about it."*
     6. *"Send me an email instead."*
     7. *"How much does this cost?"*
     8. *"Who are you? How did you get my number?"*
     9. *"Is this a sales call?"*
     10. *"I'm not interested."*
     
     *Rules for each objection response:*
     - Acknowledge and validate without arguing or becoming defensive.
     - Reframe or defer the tension.
     - Always conclude with an open question or low-friction next step (never let the conversation hit a dead end).

   - **Section E — Close Paths**:
     - **Soft Close**: Permission to send the audit PDF or 1-page summary to their email.
     - **Medium Close**: Scheduling a dedicated 15-minute screen share or phone walkthrough.
     - **Hard Close**: Transitioning when the prospect asks *"How do we get started?"* or *"What does working together look like?"*

   - **Section F — What NOT to Say**:
     - Prospect-specific warnings (e.g., avoid unprompted competitor comparisons, avoid acronyms for non-technical owners, do not lead with pricing figures, avoid sensitive personal topics from social media).

---

## 4. Output Format (Markdown Deliverable)

The generated script is saved as Markdown (`outputs/clients/{slug}/call_script.md`):

```markdown
# Call Script: [Prospect Name]
**Estimated call length:** 3-5 minutes
**Primary goal:** [soft / medium / hard close]

## Opening
> [exact words]

## The Hook
> [exact words, referencing finding #1]

## Branch Point
Ask: "[question]"
- If they say [X] → go to Branch A
- If they say [Y] → go to Branch B
- If they say [Z] → go to Branch C

## Objection Responses
### 1. "I'm too busy right now."
> [response]
Then: [next step / question]

### 2. "I don't have the budget."
> [response]
Then: [next step / question]

### 3. "I already have someone doing this."
> [response]
Then: [next step / question]

### 4. "I tried SEO/marketing before and it didn't work."
> [response]
Then: [next step / question]

### 5. "I need to think about it."
> [response]
Then: [next step / question]

### 6. "Send me an email instead."
> [response]
Then: [next step / question]

### 7. "How much does this cost?"
> [response]
Then: [next step / question]

### 8. "Who are you? How did you get my number?"
> [response]
Then: [next step / question]

### 9. "Is this a sales call?"
> [response]
Then: [next step / question]

### 10. "I'm not interested."
> [response]
Then: [next step / question]

## Close Paths
### Soft Close
> [exact words]

### Medium Close
> [exact words]

### Hard Close
> [exact words]

## What NOT to Say
- [prospect-specific warning]
- [prospect-specific warning]
```

---

## 5. Hard Operational Constraints

1. **Grounded Empirical Facts**: Every talking point and hook must reference observable data from the prospect's actual audit. Generic, templated claims are prohibited.
2. **Mandatory Momentum (No Dead Ends)**: Every single objection response must end with an open question or low-friction action. Never leave a dead silence or abrupt ending.
3. **Zero Pressure / Deception**: High-pressure tactics, artificial scarcity, fabricated countdowns, and aggressive rebuttals are strictly forbidden.
4. **Human Execution Only**: The agent creates and formats the script for human preparation. The agent never conducts phone calls autonomously.
