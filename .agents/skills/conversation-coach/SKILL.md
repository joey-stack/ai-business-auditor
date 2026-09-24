---
name: conversation-coach
description: "Reads existing LinkedIn conversations with prospects, analyzes the conversation state, and suggests the next reply to advance toward a meeting. READ-ONLY: never sends messages. Use when a prospect has replied and you need guidance on how to respond."
---

# Conversation Coach Skill (`conversation-coach`)

This skill reads existing LinkedIn conversation threads with prospects, evaluates message history, detects sentiment and objection signals, and suggests strategic, high-conversion responses to guide the conversation toward a meeting.

---

## 1. Purpose

Read a LinkedIn conversation, understand where it stands, and suggest the next reply to advance toward a meeting.

---

## 2. Input Specification

- **`prospect_name`** (`string`, required): The person or counterparty you are in active discussion with.

---

## 3. Step-by-Step Execution Process

1. Call `get_inbox` to find the message thread with this prospect.
2. Call `get_conversation` with the prospect's username to read the full message history.
3. Analyze the conversation:
   - How many messages have been exchanged?
   - Who spoke last? (you or them?)
   - What was the last message about?
   - Has the prospect asked any unanswered questions?
   - Have they shown interest signals (asked about pricing, timeline, next steps)?
   - Have they shown hesitation signals (said "maybe later", "no budget", "already have someone")?
4. Determine the conversation stage:
   - **`COLD_OPEN`**: You reached out, no reply yet.
   - **`WARMING`**: They replied with interest or an exploratory question.
   - **`OBJECTION`**: They raised a concern (pricing, timing, competing vendor).
   - **`READY`**: They asked about next steps, pricing, or availability for a call.
   - **`STALLED`**: No reply from the prospect for 5+ days after your last message.
5. Generate a suggested reply based on the stage:
   - Answer any open questions directly and transparently.
   - Acknowledge objections empathetically and offer a specific, low-commitment perspective.
   - Keep the reply concise, professional, and ending with a clear, low-friction call-to-action.

---

## 4. Output JSON Schema

```json
{
  "prospect_name": string,
  "messages_exchanged": number,
  "last_speaker": "you" | "them",
  "conversation_stage": "COLD_OPEN" | "WARMING" | "OBJECTION" | "READY" | "STALLED",
  "unanswered_questions": string[],
  "suggested_reply": string,
  "reply_reasoning": string,
  "things_to_avoid": string[],
  "recommended_next_step": string
}
```

---

## 5. Hard Constraints & Operational Safety

- **READ-ONLY Mandate**: Never call `send_message`, `send_inmail`, or any write tool. The human operator always reviews and manually sends the reply.
- **Tool Call Ceiling**: Maximum 3 LinkedIn tool calls per invocation (`get_inbox` + `get_conversation` + optional profile search).
- **Thread Not Found**: If the prospect has no existing conversation thread, return `{ "found": false, "prospect_name": string }` and conclude.
