---
name: video-generator
description: "Automatically generates a narrated walkthrough video of a prospect's website using agent-loom. Use after an audit report is complete to create a shareable video summary."
---

# Video Generator Skill (`video-generator`)

This skill automatically generates a narrated walkthrough video of a target business or prospect's website using the `agent-loom` CLI tool, creating an MP4 video artifact that can be reviewed and shared with the prospect.

---

## 1. Purpose

Generate an MP4 video walkthrough of a prospect's website to visually summarize audit findings and friction points.

---

## 2. Input Specification

- **`website_url`** (`string`, required): The target company website URL.
- **`audit_summary`** (`string`, required): The executive summary and high-impact gaps identified during the audit.
- **`prospect_name`** (`string`, optional): Business or prospect identifier used to name the output video.

---

## 3. Step-by-Step Execution Process

1. **Verify Tool Availability**:
   - The workspace utilizes the native Python Playwright browser recorder engine in `tools/record_walkthrough.py` using system-installed Google Chrome or Microsoft Edge.
   - If Playwright ffmpeg is missing, it installs automatically via:
     ```bash
     python -m playwright install ffmpeg
     ```

2. **Record Walkthrough Video**:
   - Run the custom walkthrough recorder command:
     ```bash
     python tools/record_walkthrough.py --url <website_url> --output outputs/clients/<company-slug>/walkthrough.webm
     ```

3. **Return Artifact Path**:
   - Verify the output video file exists at `outputs/clients/<company-slug>/walkthrough.webm`.
   - Return the path to the generated video file.

---

## 4. Output Schema

```json
{
  "prospect_name": string,
  "website_url": string,
  "video_path": string | null,
  "status": "completed" | "failed" | "skipped",
  "notes": string
}
```

---

## 5. Constraints & Boundaries

- **Conditional Execution Only**: Never execute automatically unless the user explicitly ran `/audit` with the `--video` flag.
- **Fail-Safe Operation**: If `agent-loom` is not installed or fails during recording, log the incident in `outputs/audit_log.csv` and proceed to the human review checkpoint without blocking report delivery.
