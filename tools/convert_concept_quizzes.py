#!/usr/bin/env python3
"""Convert existing concept HTML quizzes + hooks MD into module-bank format."""
import re, json
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── extractors ───────────────────────────────────────────────────────────────

def extract_from_html(path: Path) -> list[dict]:
    """Pull BANK questions from an old-format HTML quiz."""
    txt = path.read_text(encoding="utf-8")
    m = re.search(r'var BANK\s*=\s*(\[[\s\S]*?\]);\s*\n', txt)
    if not m:
        raise ValueError(f"No BANK in {path}")
    raw = m.group(1)
    j = re.sub(r'(?<!["\w])(\b(?:source|prompt|opts|ans|expl)\b)\s*:', r'"\1":', raw)
    j = re.sub(r',\s*([\]\}])', r'\1', j)
    pattern = re.compile(
        r'\{\s*"source"\s*:\s*("(?:[^"\\]|\\.)*")\s*,'
        r'\s*"prompt"\s*:\s*("(?:[^"\\]|\\.)*")\s*,'
        r'\s*"opts"\s*:\s*\[([^\]]*)\]\s*,'
        r'\s*"ans"\s*:\s*(\d+)\s*,'
        r'\s*"expl"\s*:\s*("(?:[^"\\]|\\.)*")\s*\}',
        re.S,
    )
    qs = []
    for qm in pattern.finditer(j):
        opts = [o.strip() for o in re.findall(r'"((?:[^"\\]|\\.)*)"', qm.group(3))]
        qs.append({
            "source": json.loads(qm.group(1)),
            "prompt": json.loads(qm.group(2)),
            "opts": opts,
            "ans": int(qm.group(4)),
            "expl": json.loads(qm.group(5)),
        })
    return qs


def extract_hooks_from_md(path: Path) -> list[dict]:
    """Parse cca-hooks-quiz.md (question + answer-key format)."""
    txt = path.read_text(encoding="utf-8")
    ak_start = txt.find("## Answer Key")
    q_text = txt[:ak_start]
    ak_text = txt[ak_start:]

    parts = re.split(r"^### Q\d+\s*$", q_text, flags=re.M)[1:]

    # Parse answer key: "1. **B** - reason text"
    answers: dict[int, dict] = {}
    for num, letter, reason in re.findall(r"(\d+)\.\s+\*\*([A-D])\*\*\s*[-–]\s*(.+)", ak_text):
        answers[int(num)] = {"letter": letter, "reason": reason.strip()}

    qs = []
    for idx, block in enumerate(parts, 1):
        lines = [l.rstrip() for l in block.strip().split("\n")]
        prompt_lines, opt_lines, in_opts = [], [], False
        for line in lines:
            if re.match(r"^[A-D]\.\s", line):
                in_opts = True
            if in_opts:
                if re.match(r"^[A-D]\.\s", line):
                    opt_lines.append(line)
            else:
                prompt_lines.append(line)

        prompt = " ".join(l for l in prompt_lines if l)
        opts = []
        for ol in opt_lines:
            m = re.match(r"^[A-D]\.\s+(.+?)$", ol)
            if m:
                opts.append(m.group(1).strip())

        if len(opts) < 4 or idx not in answers:
            print(f"  hooks Q{idx}: skipping ({len(opts)} opts, answer={'yes' if idx in answers else 'no'})")
            continue

        ak = answers[idx]
        ans_idx = ord(ak["letter"]) - ord("A")
        expl = ak["reason"]

        qs.append({
            "source": "Hooks & Workflow Control",
            "prompt": prompt,
            "opts": opts,
            "ans": ans_idx,
            "expl": expl,
        })

    return qs


# ── MD writer ─────────────────────────────────────────────────────────────────

def to_module_bank_md(questions: list[dict], module_name: str) -> str:
    letters = "ABCD"
    lines = [f"# {module_name} — Question Bank\n"]
    for i, q in enumerate(questions, 1):
        ans_letter = letters[q["ans"]]
        lines += [
            f"## Question {i}",
            q["prompt"],
            "",
        ]
        for j, opt in enumerate(q["opts"][:4]):
            lines.append(f"{letters[j]}) {opt}")
        lines += [
            "",
            "<details>",
            "<summary>Answer</summary>",
            "",
            f"**{ans_letter})** {q['expl']}",
            "",
            "</details>",
            "",
            "---",
            "",
        ]
    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

SOURCES = {
    "agentic-loops": {
        "html": ROOT / "quizzes/cca-agentic-loops-quiz.html",
        "name": "Agentic Loops",
    },
    "mcp": {
        "html": ROOT / "quizzes/cca-mcp-quiz.html",
        "name": "MCP & Tool Design",
    },
    "tool-use": {
        "html": ROOT / "quizzes/cca-tool-use-quiz.html",
        "name": "Tool Use & Extended Thinking",
    },
    "hooks": {
        "md": ROOT / "quizzes/cca-hooks-quiz.md",
        "name": "Hooks & Workflow Control",
    },
}

out_dir = ROOT / "practice-tests/concept-banks"
out_dir.mkdir(exist_ok=True)

for mod_id, cfg in SOURCES.items():
    if "html" in cfg:
        qs = extract_from_html(cfg["html"])
    else:
        qs = extract_hooks_from_md(cfg["md"])

    md = to_module_bank_md(qs, cfg["name"])
    out = out_dir / f"concept-{mod_id}.md"
    out.write_text(md, encoding="utf-8")
    print(f"  {mod_id}: {len(qs)} questions → {out.name}")

print("\nConcept bank files written.")
