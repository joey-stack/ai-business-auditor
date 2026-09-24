"""
PreToolUse hook script to enforce ethical data sourcing.
Blocks tool calls attempting to access paywalled or private intranet systems.
"""

import sys
import json
import re

DENY_DOMAINS = [
    r"bloomberg\.com",
    r"wsj\.com",
    r"ft\.com",
    r"economist\.com",
    r"theinformation\.com",
    r"reuters\.com/pro",
    r"pitchbook\.com",
    r"cbinsights\.com",
    r"localhost",
    r"127\.0\.0\.1",
    r"192\.168\.",
    r"10\.\d+\.\d+\.\d+",
]

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        args = tool_call.get("args", {})
        
        # Check URL or CommandLine or Query
        text_to_check = json.dumps(args).lower()
        
        for pattern in DENY_DOMAINS:
            if re.search(pattern, text_to_check):
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"Access blocked by Audit Standards: target matches paywalled or private domain pattern ({pattern})."
                }))
                return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        # Fallback open to avoid breaking runtime on hook parse error
        print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
