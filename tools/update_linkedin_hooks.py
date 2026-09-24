#!/usr/bin/env python3
"""
Directly update remaining hooks in generate_60_day_content.py so all 25 hooks are <= 58 chars.
"""

TARGET_HOOKS = {
    6: "The most dangerous trade metric: Revenue per Truck.",
    7: "Inside a 4-Pillar Systems Audit for a $5M fleet.",
    8: "Who answers your dispatch line at 8:30 PM?",
    9: "A 4.8-star rating means zero without review velocity.",
    10: "The psychology of contractor quoting: 3 choices.",
    11: "Run this 60-second test on your phones tonight.",
    13: "How Summit Mechanical unlocked $486k in cross-sells.",
    14: "The Deloitte Effort vs Impact Matrix for trade fleets.",
    16: "How to get 25 verified Google reviews every month.",
    17: "Stop sending flat quotes. Give customers 3 choices.",
    18: "Why single-trade fleets are losing to dual-trade.",
    19: "First freeze hits: does your dispatch collapse?",
    20: "What is your real close rate on replacement quotes?",
    21: "Stop hiring more dispatchers to fix missed calls.",
    22: "County-wide targeting burns your high-margin leads.",
    24: "The 3 software handoffs trade fleets must automate.",
    25: "What we learned auditing $45M in trade revenue.",
}

# Verify lengths
for k, v in TARGET_HOOKS.items():
    assert len(v) <= 58, f"{k}: {len(v)} > 58"

with open("generate_60_day_content.py", "r", encoding="utf-8") as f:
    code = f.read()

import sys
sys.path.insert(0, ".")
from generate_60_day_content import build_data
data = build_data()
posts = data[7:]

for i, p in enumerate(posts):
    post_idx = i + 1
    if post_idx in TARGET_HOOKS:
        old_hook = p[5]
        new_hook = TARGET_HOOKS[post_idx]
        code = code.replace(f'"{old_hook}"', f'"{new_hook}"')
        code = code.replace(f'"{old_hook}\\n\\n', f'"{new_hook}\\n\\n')

with open("generate_60_day_content.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated all remaining hooks in generate_60_day_content.py!")
