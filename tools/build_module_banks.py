#!/usr/bin/env python3
"""Build 30-question module banks for prep-style CCA exam rotation."""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
PRACTICE_DIR = ROOT / "practice-tests"
MODULE_DIR = PRACTICE_DIR / "module-banks"
MANIFEST_PATH = MODULE_DIR / "manifest.json"

MODULES = [
    {
        "id": "customer-support",
        "name": "Customer Support Resolution Agent",
        "primary": ["test-03-hooks-workflows.md", "test-09-context-reliability.md"],
        "scenario": "A",
        "keywords": ["refund", "customer", "escalat", "lookup_order", "get_customer", "support"],
    },
    {
        "id": "code-generation",
        "name": "Code Generation with Claude Code",
        "primary": ["test-05-claude-code-config.md"],
        "scenario": "B",
        "keywords": ["claude.md", "skills", "commands", "plan mode", "codebase", "rules"],
    },
    {
        "id": "multi-agent-research",
        "name": "Multi-Agent Research System",
        "primary": ["test-02-multi-agent.md", "test-09-context-reliability.md"],
        "scenario": "C",
        "keywords": ["coordinator", "subagent", "synthesis", "partition", "coverage", "research"],
    },
    {
        "id": "developer-productivity",
        "name": "Developer Productivity with Claude",
        "primary": ["test-04-tool-design-mcp.md", "test-01-agentic-loops.md"],
        "scenario": "D",
        "keywords": ["tool", "mcp", "workflow", "developer", "explore", "automation"],
    },
    {
        "id": "ci-cd",
        "name": "Claude Code for CI/CD",
        "primary": ["test-06-plan-mode-cicd.md"],
        "scenario": "E",
        "keywords": ["ci", "pipeline", "batch", "sync", "review", "pre-merge", "-p"],
    },
    {
        "id": "structured-extraction",
        "name": "Structured Data Extraction",
        "primary": ["test-07-prompt-engineering.md", "test-08-validation-multipass.md", "test-10-advanced-context.md"],
        "scenario": "F",
        "keywords": ["schema", "json", "validation", "extraction", "field", "retry", "document"],
    },
]

TARGET_PER_MODULE = 30


@dataclass
class Q:
    qid: str
    prompt: str
    options: Dict[str, str]
    answer: str
    explanation: str
    source: str
    scenario: str | None = None


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_question_blocks(path: Path) -> List[Q]:
    text = path.read_text(encoding="utf-8")
    heading_regex = re.compile(r"^(## Question \d+|### Q\d+)\s*$", re.M)
    matches = list(heading_regex.finditer(text))
    scenario_headers = list(re.finditer(r"^## Scenario ([A-F]):", text, flags=re.M))

    def scenario_for_pos(pos: int) -> str | None:
        if not scenario_headers:
            return None
        hit = None
        for h in scenario_headers:
            if h.start() <= pos:
                hit = h.group(1)
            else:
                break
        return hit

    rows: List[Q] = []
    for idx, m in enumerate(matches):
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        options_m = list(re.finditer(r"^([A-D])\)\s+(.*)$", block, flags=re.M))
        if len(options_m) < 4:
            continue
        prompt = norm(block[: options_m[0].start()])
        options = {om.group(1): norm(om.group(2)) for om in options_m[:4]}
        ans_m = re.search(r"\*\*([A-D])\)\*\*", block)
        if not ans_m:
            continue
        answer = ans_m.group(1)
        exp_m = re.search(r"<details>.*?<summary>Answer</summary>(.*?)</details>", block, flags=re.S)
        explanation = norm(re.sub(r"<.*?>", " ", exp_m.group(1))) if exp_m else ""
        qn = re.search(r"(\d+)", m.group(1))
        num = qn.group(1) if qn else str(idx + 1)
        rows.append(
            Q(
                qid=f"{path.stem}:{num}",
                prompt=prompt,
                options=options,
                answer=answer,
                explanation=explanation,
                source=str(path.relative_to(ROOT)),
                scenario=scenario_for_pos(m.start()),
            )
        )
    return rows


def write_bank(path: Path, title: str, questions: List[Q]) -> None:
    lines = [f"# {title}", "", f"Auto-generated bank with {len(questions)} questions.", ""]
    for i, q in enumerate(questions, start=1):
        lines.append(f"## Question {i}")
        lines.append(q.prompt)
        lines.append("")
        for k in ["A", "B", "C", "D"]:
            lines.append(f"{k}) {q.options[k]}")
        lines.append("")
        lines.append("<details><summary>Answer</summary>")
        lines.append(f"**{q.answer})** {q.explanation} (source: {q.source})")
        lines.append("</details>")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def score_question(q: Q, module: dict, primary_sources: set[str]) -> int:
    score = 0
    q_prompt = q.prompt.lower()
    if q.source.split("/")[-1] in primary_sources:
        score += 10
    if q.scenario == module["scenario"]:
        score += 8
    for kw in module["keywords"]:
        if kw in q_prompt:
            score += 1
    return score


def main() -> None:
    MODULE_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(list(PRACTICE_DIR.glob("test-*.md")) + [PRACTICE_DIR / "full-exam-01.md"])
    pool: List[Q] = []
    for f in files:
        pool.extend(parse_question_blocks(f))

    by_qid = {q.qid: q for q in pool}
    all_q = list(by_qid.values())

    manifest = {
        "target_per_module": TARGET_PER_MODULE,
        "generated_from": [str(f.relative_to(ROOT)) for f in files],
        "modules": [],
    }

    rng = random.Random(42)
    for module in MODULES:
        primary_sources = set(module["primary"])
        scored = sorted(
            all_q,
            key=lambda q: (score_question(q, module, primary_sources), q.qid),
            reverse=True,
        )

        selected: List[Q] = []
        seen = set()

        # phase 1: take top strong matches
        for q in scored:
            if q.qid in seen:
                continue
            if score_question(q, module, primary_sources) < 3:
                continue
            selected.append(q)
            seen.add(q.qid)
            if len(selected) >= TARGET_PER_MODULE:
                break

        # phase 2: fill up with remaining strongest
        if len(selected) < TARGET_PER_MODULE:
            for q in scored:
                if q.qid in seen:
                    continue
                selected.append(q)
                seen.add(q.qid)
                if len(selected) >= TARGET_PER_MODULE:
                    break

        # stable shuffle for better rotation experience
        rng.shuffle(selected)
        selected = selected[:TARGET_PER_MODULE]

        bank_filename = f"module-{module['id']}.md"
        bank_path = MODULE_DIR / bank_filename
        write_bank(bank_path, f"Module Bank: {module['name']}", selected)

        manifest["modules"].append(
            {
                "id": module["id"],
                "name": module["name"],
                "path": str(bank_path.relative_to(ROOT)),
                "question_count": len(selected),
                "scenario": module["scenario"],
            }
        )

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST_PATH}")
    for m in manifest["modules"]:
        print(f"{m['id']}: {m['question_count']} -> {m['path']}")


if __name__ == "__main__":
    main()
