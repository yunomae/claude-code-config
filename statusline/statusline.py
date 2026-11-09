#!/usr/bin/env python3
"""Claude Code statusLine command. Reads JSON payload from stdin, prints summary."""
import argparse
import json
import os
import sys
import time

CYAN, GREEN, YELLOW, RED = "36", "32", "33", "31"
SEPARATOR = "   "  # 項目間は空白3つ。記号は使わず色で区別する


def paint(text, code):
    """ANSI カラーを付ける。NO_COLOR が設定されている場合は無着色。"""
    if os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def format_remaining(resets_at, now):
    """リセットまでの残り時間を '2h10m' / '3d4h' / '35m' 形式で返す。不明なら None。"""
    if not isinstance(resets_at, (int, float)):
        return None
    sec = int(resets_at - now)
    if sec <= 0:
        return None
    minutes = sec // 60
    days, rem = divmod(minutes, 60 * 24)
    hours, mins = divmod(rem, 60)
    if days:
        return f"{days}d{hours}h"
    if hours:
        return f"{hours}h{mins:02d}m"
    return f"{mins}m"


def format_limit(label, window, threshold, now):
    """rate_limits の1窓を '5h 24% (resets in 2h10m)' 形式にする。使用率が無ければ None。"""
    used = (window or {}).get("used_percentage")
    if not isinstance(used, (int, float)):
        return None
    over = used >= threshold
    text = f"{label} {used:.0f}%{'!' if over else ''}"
    remaining = format_remaining(window.get("resets_at"), now)
    if remaining:
        text += f" (resets in {remaining})"
    return paint(text, RED if over else YELLOW)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--threshold", type=float, default=70.0,
        help="コンテキスト使用率がこの値(%%）以上になると '!' を表示 (デフォルト: 70)",
    )
    parser.add_argument(
        "--limit-threshold", type=float, default=80.0,
        help="5時間/週次の使用率がこの値(%%）以上になると '!' を表示 (デフォルト: 80)",
    )
    args = parser.parse_args()

    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    model_name = (payload.get("model") or {}).get("display_name") or "unknown"
    effort = (payload.get("effort") or {}).get("level")
    cw = payload.get("context_window") or {}
    used_pct = cw.get("used_percentage")

    parts = [paint(f"{model_name} {effort}" if effort else model_name, CYAN)]
    if isinstance(used_pct, (int, float)):
        over = used_pct >= args.threshold
        text = f"ctx {used_pct:.0f}%{'!' if over else ''}"
        parts.append(paint(text, RED if over else GREEN))

    # rate_limits は claude.ai の Pro/Max/Ultra 契約でのみ、最初の API 応答後に入る。
    # 各窓は個別に欠落しうるため、あるものだけ表示する。
    limits = payload.get("rate_limits") or {}
    now = time.time()
    for label, key in (("5h", "five_hour"), ("7d", "seven_day")):
        text = format_limit(label, limits.get(key), args.limit_threshold, now)
        if text:
            parts.append(text)

    print(SEPARATOR.join(parts))


if __name__ == "__main__":
    main()
