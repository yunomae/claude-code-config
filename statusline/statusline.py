#!/usr/bin/env python3
"""Claude Code statusLine command. Reads JSON payload from stdin, prints summary."""
import json
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    model_name = (payload.get("model") or {}).get("display_name") or "unknown"
    effort = (payload.get("effort") or {}).get("level")
    cw = payload.get("context_window") or {}
    used_pct = cw.get("used_percentage")
    exceeds_200k = bool(payload.get("exceeds_200k_tokens"))

    parts = [model_name]
    if effort:
        parts.append(effort)
    if isinstance(used_pct, (int, float)):
        marker = "!" if exceeds_200k else ""
        parts.append(f"{used_pct:.0f}%{marker}")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
