#!/usr/bin/env python3
"""Unified CLI for the CCA study workspace."""

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
PLAN_JSON = ROOT / "calendar" / "cca_daily_plan.json"
PRACTICE_DIR = ROOT / "practice-tests"
LOG_FILE = ROOT / "logs" / "cca_quiz_attempts.jsonl"
OBSIDIAN_RULES = ROOT / "docs" / "obsidian-rules.md"


def load_plan() -> dict:
    return json.loads(PLAN_JSON.read_text(encoding="utf-8"))


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_reading_items(reading_text: str) -> list[str]:
    parts = [p.strip() for p in reading_text.split(" ; ")]
    items = [normalize_whitespace(p) for p in parts if p.strip()]
    return items


def count_questions_in_markdown(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r"^(## Question \d+|### Q\d+)\s*$", text, flags=re.M))


def run_subprocess(command: list[str], dry_run: bool = False) -> int:
    printable = " ".join(command)
    if dry_run:
        print(f"[dry-run] {printable}")
        return 0
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_list(_args: argparse.Namespace) -> int:
    print("CCA CLI actions")
    print("  read      Show the study plan and reading checklist for a date")
    print("  plan      Show a date range plan table")
    print("  content   List available practice-test content and question counts")
    print("  test      Run interactive test mode (delegates to tools/cca_quiz.py)")
    print("  sim       Run full 60-question, 120-minute simulation")
    print("  stats     Show recent attempt metrics from logs")
    print("  obsidian  Show Obsidian rules reference path")
    print("")
    print("Examples")
    print("  python3 tools/cca.py read --date 2026-05-09")
    print("  python3 tools/cca.py test --date 2026-05-09 --count 20 --timed-minutes 90")
    print("  python3 tools/cca.py sim --seed 42")
    print("  python3 tools/cca.py content")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    plan = load_plan()
    target = args.date or str(date.today())
    day = plan.get(target)
    if not day:
        print(f"No plan entry for {target}")
        return 1

    print(f"Date: {target}")
    print(f"Focus: {day.get('focus', '')}")
    print("Reading checklist:")
    for idx, item in enumerate(split_reading_items(day.get("reading", "")), start=1):
        print(f"  {idx}. {item}")

    review_items = day.get("review_slot_4pm") or []
    if review_items:
        print("4-5 PM review block:")
        for item in review_items:
            print(f"  - {item}")

    print("Test sources:")
    for src in day.get("test_sources", []):
        print(f"  - {src}")
    print("Suggested test command:")
    print(f"  {day.get('test_command', '').strip()}")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    plan = load_plan()
    keys = sorted(plan.keys())
    if not keys:
        print("No schedule data found.")
        return 1

    start = args.from_date or keys[0]
    end = args.to_date or keys[-1]
    selected = [k for k in keys if start <= k <= end]
    if not selected:
        print(f"No entries in range {start} to {end}")
        return 1

    print(f"Plan window: {start} -> {end}")
    for d in selected:
        day = plan[d]
        reading_items = split_reading_items(day.get("reading", ""))
        first_read = reading_items[0] if reading_items else "-"
        print(f"- {d} | {day.get('kind', '')} | {day.get('focus', '')}")
        print(f"  read: {first_read}")
        print(f"  test: {day.get('test_command', '')}")
    return 0


def cmd_content(_args: argparse.Namespace) -> int:
    files = sorted(PRACTICE_DIR.glob("*.md"))
    if not files:
        print("No practice-test files found.")
        return 1

    print("Practice test bank")
    total = 0
    for f in files:
        q_count = count_questions_in_markdown(f)
        total += q_count
        print(f"- {f.relative_to(ROOT)} ({q_count} questions)")
    print(f"Total parsed question headings: {total}")
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    command = ["python3", "tools/cca_quiz.py"]
    if args.date:
        command += ["--date", args.date]
    if args.count is not None:
        command += ["--count", str(args.count)]
    if args.timed_minutes is not None:
        command += ["--timed-minutes", str(args.timed_minutes)]
    if args.seed is not None:
        command += ["--seed", str(args.seed)]
    if args.reveal:
        command.append("--reveal")
    for src in args.source:
        command += ["--source", src]
    return run_subprocess(command, dry_run=args.dry_run)


def cmd_sim(args: argparse.Namespace) -> int:
    command = ["python3", "tools/cca_quiz.py", "--full-sim"]
    if args.seed is not None:
        command += ["--seed", str(args.seed)]
    if args.reveal:
        command.append("--reveal")
    return run_subprocess(command, dry_run=args.dry_run)


def load_attempts() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    rows = []
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def cmd_stats(args: argparse.Namespace) -> int:
    rows = load_attempts()
    if not rows:
        print(f"No attempt logs found at {LOG_FILE}")
        return 0

    rows = rows[-args.last :]
    scores = [r.get("score_1000", 0) for r in rows]
    passes = [r.get("passed", False) for r in rows]
    latest = rows[-1]
    latest_date = latest.get("date") or latest.get("started_at", "")
    if latest_date:
        try:
            latest_date = datetime.fromisoformat(latest_date.replace("Z", "+00:00")).isoformat()
        except ValueError:
            pass

    print(f"Recent attempts: {len(rows)}")
    print(f"Average score: {mean(scores):.1f}/1000")
    print(f"Passes: {sum(1 for p in passes if p)}/{len(rows)}")
    print(f"Best score: {max(scores)}/1000")
    print(f"Latest: {latest_date}")
    print("Last scores: " + ", ".join(str(s) for s in scores))
    return 0


def cmd_obsidian(_args: argparse.Namespace) -> int:
    print("Obsidian rules reference")
    print(f"- {OBSIDIAN_RULES}")
    if OBSIDIAN_RULES.exists():
        print("- status: present")
    else:
        print("- status: missing")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CCA workspace command center (read, test, plan, content, stats, obsidian)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("list", help="List available actions and examples")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("read", help="Show reading checklist and test sources for a date")
    sp.add_argument("--date", help="YYYY-MM-DD (defaults to today)")
    sp.set_defaults(func=cmd_read)

    sp = sub.add_parser("plan", help="Show plan entries in a date range")
    sp.add_argument("--from-date", help="YYYY-MM-DD")
    sp.add_argument("--to-date", help="YYYY-MM-DD")
    sp.set_defaults(func=cmd_plan)

    sp = sub.add_parser("content", help="List available practice content and question counts")
    sp.set_defaults(func=cmd_content)

    sp = sub.add_parser("test", help="Run interactive test mode")
    sp.add_argument("--date", help="YYYY-MM-DD; uses schedule-mapped sources")
    sp.add_argument("--source", action="append", default=[], help="Relative practice-test file (repeatable)")
    sp.add_argument("--count", type=int, default=10, help="Question count")
    sp.add_argument("--timed-minutes", type=int, default=20, help="Timer in minutes")
    sp.add_argument("--seed", type=int, help="Random seed")
    sp.add_argument("--reveal", action="store_true", help="Reveal correctness after each question")
    sp.add_argument("--dry-run", action="store_true", help="Print the command instead of running it")
    sp.set_defaults(func=cmd_test)

    sp = sub.add_parser("sim", help="Run full 60Q/120m simulation")
    sp.add_argument("--seed", type=int, help="Random seed")
    sp.add_argument("--reveal", action="store_true", help="Reveal correctness after each question")
    sp.add_argument("--dry-run", action="store_true", help="Print the command instead of running it")
    sp.set_defaults(func=cmd_sim)

    sp = sub.add_parser("stats", help="Show score stats from recent attempts")
    sp.add_argument("--last", type=int, default=10, help="Number of most recent attempts to analyze")
    sp.set_defaults(func=cmd_stats)

    sp = sub.add_parser("obsidian", help="Show Obsidian rules reference path")
    sp.set_defaults(func=cmd_obsidian)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
