"""
PreInvocation hook script to inject the reasoning scaffold reminder before model turns.
"""

import sys
import json

def main():
    try:
        # PreInvocation returns injectSteps with ephemeralMessage
        reminder_payload = {
            "injectSteps": [
                {
                    "ephemeralMessage": "AUDIT GOVERNANCE MANDATE: Every pillar score (1-10) must be substantiated using the 4-step Reasoning Scaffold (Step A: Evidence -> Step B: Expected State -> Step C: Gap -> Step D: Score). Subagents must receive the complete profile explicitly."
                }
            ]
        }
        print(json.dumps(reminder_payload))
    except Exception:
        print(json.dumps({"injectSteps": []}))

if __name__ == "__main__":
    main()
