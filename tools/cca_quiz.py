#!/usr/bin/env python3
import argparse
import json
import random
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[1]
PRACTICE_DIR = ROOT / "practice-tests"
PLAN_JSON = ROOT / "calendar" / "cca_daily_plan.json"
ATTEMPT_LOG = ROOT / "logs" / "cca_quiz_attempts.jsonl"


@dataclass
class Question:
    qid: str
    source: str
    prompt: str
    options: dict
    answer: str
    explanation: str


def normalize_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_markdown_questions(path: Path) -> List[Question]:
    text = path.read_text(encoding="utf-8")
    heading_regex = re.compile(r"^(## Question \d+|### Q\d+)\s*$", re.M)
    matches = list(heading_regex.finditer(text))
    questions: List[Question] = []

    for idx, m in enumerate(matches):
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end].strip()

        option_matches = list(re.finditer(r"^([A-D])\)\s+(.*)$", block, flags=re.M))
        if len(option_matches) < 4:
            continue

        prompt = block[: option_matches[0].start()].strip()
        options = {}
        for om in option_matches[:4]:
            options[om.group(1)] = normalize_text(om.group(2))

        answer_match = re.search(r"\*\*([A-D])\)\*\*", block)
        if not answer_match:
            continue

        answer = answer_match.group(1)
        explanation = ""
        details_match = re.search(r"<details>.*?<summary>Answer</summary>(.*?)</details>", block, flags=re.S)
        if details_match:
            explanation = normalize_text(re.sub(r"<.*?>", " ", details_match.group(1)))

        qnum_match = re.search(r"(\d+)", m.group(1))
        qnum = qnum_match.group(1) if qnum_match else str(idx + 1)
        qid = f"{path.stem}:{qnum}"

        questions.append(
            Question(
                qid=qid,
                source=str(path.relative_to(ROOT)),
                prompt=normalize_text(prompt),
                options=options,
                answer=answer,
                explanation=explanation,
            )
        )

    return questions


def load_all_questions(files: List[Path]) -> List[Question]:
    seen = set()
    bank: List[Question] = []
    for f in files:
        for q in parse_markdown_questions(f):
            if q.qid in seen:
                continue
            seen.add(q.qid)
            bank.append(q)
    return bank


def resolve_sources(args) -> List[Path]:
    if args.source:
        return [ROOT / s for s in args.source]

    if args.date:
        plan = json.loads(PLAN_JSON.read_text(encoding="utf-8"))
        day = plan.get(args.date)
        if not day:
            raise SystemExit(f"No schedule entry for {args.date} in {PLAN_JSON}")
        return [ROOT / s for s in day["test_sources"]]

    return sorted(PRACTICE_DIR.glob("test-*.md"))


def run_quiz(questions: List[Question], timed_minutes: int, reveal: bool) -> dict:
    total = len(questions)
    correct = 0
    responses = []
    start = datetime.now()
    deadline = None
    if timed_minutes > 0:
        deadline = start.timestamp() + timed_minutes * 60

    print(f"\nCCA Interactive Quiz")
    print(f"Questions: {total}")
    if timed_minutes > 0:
        print(f"Time limit: {timed_minutes} minutes")
    print("Pass threshold: 720/1000")
    print("-" * 72)

    for i, q in enumerate(questions, start=1):
        if deadline and datetime.now().timestamp() > deadline:
            print("\nTime is up.")
            break

        print(f"\nQ{i}/{total} [{q.source}]\n{q.prompt}\n")
        for key in ["A", "B", "C", "D"]:
            print(f"  {key}) {q.options.get(key, '')}")

        while True:
            ans = input("Your answer (A/B/C/D, or Q to quit): ").strip().upper()
            if ans in {"A", "B", "C", "D", "Q"}:
                break
            print("Invalid input. Enter A, B, C, D, or Q.")

        if ans == "Q":
            print("\nQuiz stopped by user.")
            break

        is_correct = ans == q.answer
        if is_correct:
            correct += 1

        responses.append(
            {
                "qid": q.qid,
                "source": q.source,
                "selected": ans,
                "correct": q.answer,
                "is_correct": is_correct,
                "explanation": q.explanation,
            }
        )

        if reveal:
            print(f"=> {'Correct' if is_correct else f'Incorrect (correct: {q.answer})'}")

    answered = len(responses)
    score_1000 = int(round((correct / answered) * 1000)) if answered else 0
    passed = score_1000 >= 720

    print("\n" + "=" * 72)
    print(f"Answered: {answered}/{total}")
    print(f"Correct:  {correct}/{answered}")
    print(f"Score:    {score_1000}/1000")
    print(f"Result:   {'PASS' if passed else 'RETEST'}")
    print("=" * 72)

    if not reveal and responses:
        print("\nReview:")
        for r in responses:
            if r["is_correct"]:
                continue
            print(f"- {r['qid']}: picked {r['selected']}, correct {r['correct']}")

    return {
        "started_at": start.replace(tzinfo=timezone.utc).isoformat(),
        "ended_at": datetime.now(tz=timezone.utc).isoformat(),
        "total": total,
        "answered": answered,
        "correct": correct,
        "score_1000": score_1000,
        "passed": passed,
        "responses": responses,
    }


def write_attempt_log(payload: dict):
    ATTEMPT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ATTEMPT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Interactive CCA test runner with grading and retests")
    parser.add_argument("--date", help="YYYY-MM-DD; loads scheduled sources from calendar/cca_daily_plan.json")
    parser.add_argument("--source", action="append", help="Relative source file path (repeatable)")
    parser.add_argument("--count", type=int, default=10, help="Number of questions to ask")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--timed-minutes", type=int, default=20, help="Timer in minutes (0 disables)")
    parser.add_argument("--reveal", action="store_true", help="Show correctness immediately per question")
    parser.add_argument("--full-sim", action="store_true", help="Run a 60-question, 120-minute proctored simulation")
    args = parser.parse_args()

    sources = resolve_sources(args)
    for s in sources:
        if not s.exists():
            raise SystemExit(f"Source not found: {s}")

    bank = load_all_questions(sources)
    if not bank:
        raise SystemExit("No questions parsed from selected sources.")

    if args.full_sim:
        target_count = 60
        timed = 120
        pool = load_all_questions(sorted(PRACTICE_DIR.glob("*.md")))
        if len(pool) < target_count:
            raise SystemExit(f"Not enough questions for full sim: need {target_count}, found {len(pool)}")
        bank = pool
    else:
        target_count = max(1, min(args.count, len(bank)))
        timed = args.timed_minutes

    rng = random.Random(args.seed)
    selected = rng.sample(bank, target_count)

    result = run_quiz(selected, timed, args.reveal)
    result.update(
        {
            "mode": "full_sim" if args.full_sim else "daily",
            "sources": [str(s.relative_to(ROOT)) for s in sources],
            "seed": args.seed,
        }
    )
    if args.date:
        result["date"] = args.date

    write_attempt_log(result)
    print(f"\nAttempt saved to {ATTEMPT_LOG}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
