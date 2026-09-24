"""
PostToolUse hook script to log MCP enrichment calls to outputs/enrichment_log.jsonl.
"""

import sys
import json
import os
import datetime

def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input else {}
        
        step_idx = payload.get("stepIdx")
        error = payload.get("error")
        tool_name = payload.get("toolName", "enrichment_tool")
        args = payload.get("args", {})
        
        log_entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "step_idx": step_idx,
            "tool_name": tool_name,
            "args": args,
            "success": error is None or error == "",
            "error": error if error else None
        }
        
        # Ensure outputs/ exists
        os.makedirs("outputs", exist_ok=True)
        log_path = os.path.join("outputs", "enrichment_log.jsonl")
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
            
    except Exception:
        pass
    finally:
        # PostToolUse expects empty JSON object on stdout
        print(json.dumps({}))

if __name__ == "__main__":
    main()
