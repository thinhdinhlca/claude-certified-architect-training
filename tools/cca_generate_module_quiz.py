#!/usr/bin/env python3
"""Generate self-contained HTML quiz files from module bank Markdown files.

Usage:
    python tools/cca_generate_module_quiz.py                     # generate all 6
    python tools/cca_generate_module_quiz.py --module ci-cd      # single module
    python tools/cca_generate_module_quiz.py --output-dir quizzes  # default
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "practice-tests" / "module-banks" / "manifest.json"

BANK_SIZE = 30
QUESTIONS_PER_ATTEMPT = 20
TIMER_MINUTES = 60
PASS_SCORE = 1000
REQUIRED_PASSES = 2

# Concept banks (narrower drills; stored separately from scenario modules)
CONCEPT_MODULES = [
    # Full 30Q rotation quizzes (converted from existing HTML quizzes)
    {"id": "agentic-loops",       "name": "Agentic Loops",                 "path": "practice-tests/concept-banks/concept-agentic-loops.md"},
    {"id": "mcp",                 "name": "MCP & Tool Design",             "path": "practice-tests/concept-banks/concept-mcp.md"},
    {"id": "tool-use",            "name": "Tool Use & Extended Thinking",  "path": "practice-tests/concept-banks/concept-tool-use.md"},
    {"id": "hooks",               "name": "Hooks & Workflow Control",      "path": "practice-tests/concept-banks/concept-hooks.md"},
    # Full 30Q rotation quizzes (new exam-pattern banks)
    {"id": "context-isolation",   "name": "Context Isolation",             "path": "practice-tests/concept-banks/concept-context-isolation.md"},
    {"id": "error-propagation",   "name": "Error Propagation",             "path": "practice-tests/concept-banks/concept-error-propagation.md"},
    {"id": "batch-vs-sync",       "name": "Batch vs Sync API",             "path": "practice-tests/concept-banks/concept-batch-vs-sync.md"},
    {"id": "few-shot-patterns",   "name": "Few-Shot & Prompt Patterns",    "path": "practice-tests/concept-banks/concept-few-shot-patterns.md"},
    # 10Q concept drills (from practice-tests/test-*.md banks)
    {"id": "agentic-loops-drill",  "name": "Agentic Loops Drill",        "path": "practice-tests/test-01-agentic-loops.md",         "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "multi-agent-systems",  "name": "Multi-Agent Systems",        "path": "practice-tests/test-02-multi-agent.md",           "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "hooks-workflows-drill","name": "Hooks & Workflows Drill",    "path": "practice-tests/test-03-hooks-workflows.md",       "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "tool-design-mcp-drill","name": "Tool Design & MCP Drill",    "path": "practice-tests/test-04-tool-design-mcp.md",       "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "claude-code-config",   "name": "Claude Code Configuration",  "path": "practice-tests/test-05-claude-code-config.md",    "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "plan-mode-cicd",       "name": "Plan Mode & CI/CD",          "path": "practice-tests/test-06-plan-mode-cicd.md",        "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "prompt-engineering",   "name": "Prompt Engineering",         "path": "practice-tests/test-07-prompt-engineering.md",    "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "validation-multipass", "name": "Validation & Multi-pass",    "path": "practice-tests/test-08-validation-multipass.md",  "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "context-reliability",  "name": "Context Reliability",        "path": "practice-tests/test-09-context-reliability.md",   "questions_per_attempt": 10, "timer_minutes": 25},
    {"id": "advanced-context",     "name": "Advanced Context",           "path": "practice-tests/test-10-advanced-context.md",      "questions_per_attempt": 10, "timer_minutes": 25},
]

# Accent colors per module: (light, dark)
ACCENT_COLORS = {
    "customer-support":      ("#a78bfa", "#7c3aed"),
    "code-generation":       ("#60a5fa", "#3b82f6"),
    "multi-agent-research":  ("#34d399", "#059669"),
    "developer-productivity": ("#fb923c", "#ea580c"),
    "ci-cd":                 ("#f43f5e", "#e11d48"),
    "structured-extraction": ("#fbbf24", "#d97706"),
    # concept quizzes — full 30Q rotation
    "agentic-loops":         ("#38bdf8", "#0284c7"),
    "mcp":                   ("#2dd4bf", "#0d9488"),
    "tool-use":              ("#fbbf24", "#b45309"),
    "hooks":                 ("#c084fc", "#9333ea"),
    "context-isolation":     ("#818cf8", "#4f46e5"),
    "error-propagation":     ("#f87171", "#dc2626"),
    "batch-vs-sync":         ("#4ade80", "#16a34a"),
    "few-shot-patterns":     ("#fb923c", "#c2410c"),
    # concept drills — 10Q
    "agentic-loops-drill":   ("#38bdf8", "#0284c7"),
    "multi-agent-systems":   ("#34d399", "#059669"),
    "hooks-workflows-drill": ("#c084fc", "#9333ea"),
    "tool-design-mcp-drill": ("#2dd4bf", "#0d9488"),
    "claude-code-config":    ("#60a5fa", "#3b82f6"),
    "plan-mode-cicd":        ("#f43f5e", "#e11d48"),
    "prompt-engineering":    ("#fb923c", "#ea580c"),
    "validation-multipass":  ("#a78bfa", "#7c3aed"),
    "context-reliability":   ("#2dd4bf", "#0d9488"),
    "advanced-context":      ("#f472b6", "#db2777"),
}

# Domain tags per module
DOMAIN_TAGS = {
    "customer-support":       ["Tool Selection", "Escalation Criteria", "Context Management", "Summarization", "Multi-Concern Routing", "Validation"],
    "code-generation":        ["CLAUDE.md", "Plan Mode", "Skills & Commands", "Codebase Context", "Code Review", "CI/CD Integration"],
    "multi-agent-research":   ["Coordinator/Subagent", "Synthesis", "Coverage Partitioning", "Context Reliability", "Multi-Agent Trust", "Orchestration"],
    "developer-productivity": ["Tool Design", "MCP", "Agentic Loops", "Workflow Automation", "Permission Model", "Developer UX"],
    "ci-cd":                  ["Plan Mode", "CI/CD Pipelines", "Batch Processing", "Pre-merge Review", "Non-interactive", "Automation"],
    "structured-extraction":  ["Schema Design", "JSON Validation", "Prompt Engineering", "Multi-pass", "Advanced Context", "Document Extraction"],
    # concept quizzes — full 30Q rotation
    "agentic-loops":          ["stop_reason", "Tool Execution", "Context History", "Iteration Control", "Error Handling", "Loop Termination"],
    "mcp":                    ["MCP Protocol", "Host/Client/Server", "Transport", "Initialization", "Tool Exposure", "Security"],
    "tool-use":               ["Tool Definitions", "Extended Thinking", "Adaptive Thinking", "tool_choice", "Multi-turn", "Computer Use"],
    "hooks":                  ["PreToolUse", "PostToolUse", "HTTP Hooks", "Async Hooks", "Permission Events", "Lifecycle Events"],
    "context-isolation":      ["context: fork", "CLAUDE.md", "Skills", ".claude/rules/", "allowed-tools", "Explore Subagent"],
    "error-propagation":      ["Error Taxonomy", "Local Recovery", "Structured Errors", "Coverage Annotations", "Partial Success", "Trust Levels"],
    "batch-vs-sync":          ["Message Batches", "Batch Incompatibilities", "custom_id", "Result Polling", "CI Mode", "Non-interactive"],
    "few-shot-patterns":      ["Few-Shot", "Self-Critique", "Preprocessing", "Chain-of-Thought", "Prompt Boundaries", "Extended Thinking"],
    # concept drills — 10Q
    "agentic-loops-drill":    ["stop_reason", "Loop Termination", "Tool Execution", "Iteration Control", "Error Handling"],
    "multi-agent-systems":    ["Coordinator/Subagent", "Parallel Execution", "Context Passing", "Trust Levels", "Error Propagation"],
    "hooks-workflows-drill":  ["PreToolUse", "PostToolUse", "Hook Ordering", "Programmatic Prerequisites", "Session Safety"],
    "tool-design-mcp-drill":  ["Tool Naming", "Tool Schema", "MCP Primitives", "Tool Selection", "Description Quality"],
    "claude-code-config":     ["CLAUDE.md", "Settings Scope", "Allowed Tools", "MCP Config", "Permission Model"],
    "plan-mode-cicd":         ["Plan Mode", "CI/CD", "Non-interactive", "Batch Processing", "Output Contracts"],
    "prompt-engineering":     ["Few-shot", "Self-critique", "Chain-of-Thought", "Structured Output", "Prompt Boundaries"],
    "validation-multipass":   ["Multi-pass Validation", "Schema Enforcement", "Retry Logic", "Error Recovery"],
    "context-reliability":    ["Context Isolation", "fork_session", "Skills", "CLAUDE.md Scope", "Token Pressure"],
    "advanced-context":       ["Extended Context", "Compaction", "Summarization", "Context Windows", "Retrieval"],
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_markdown(path: Path, module_name: str) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    heading_regex = re.compile(r"^(## Question \d+|### Q\d+)\s*$", re.M)
    matches = list(heading_regex.finditer(text))
    rows: list[dict] = []

    for idx, m in enumerate(matches):
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end].strip()

        option_matches = list(re.finditer(r"^([A-D])\)\s+(.*)$", block, flags=re.M))
        if len(option_matches) < 4:
            continue

        prompt = norm(block[: option_matches[0].start()])
        options = [norm(om.group(2)) for om in option_matches[:4]]

        ans = re.search(r"\*\*([A-D])\)\*\*", block)
        if not ans:
            continue
        answer_idx = ord(ans.group(1)) - ord("A")

        details = re.search(
            r"<details>.*?<summary>Answer</summary>(.*?)</details>", block, flags=re.S
        )
        if details:
            raw_expl = details.group(1)
            # Strip the bold answer letter prefix: **X)** ...
            raw_expl = re.sub(r"^\s*\*\*[A-D]\)\*\*\s*", "", raw_expl.strip())
            # Strip (source: ...) suffix
            raw_expl = re.sub(r"\s*\(source:[^)]+\)\s*$", "", raw_expl.strip())
            explanation = norm(re.sub(r"<[^>]+>", " ", raw_expl))
        else:
            explanation = ""

        rows.append(
            {
                "source": module_name,
                "prompt": prompt,
                "opts": options,
                "ans": answer_idx,
                "expl": explanation,
            }
        )

    return rows


def generate_html(
    module_id: str,
    module_name: str,
    bank: list[dict],
    questions_per_attempt: int = QUESTIONS_PER_ATTEMPT,
    timer_minutes: int = TIMER_MINUTES,
) -> str:
    # Allow per-module overrides of the global constants (used verbatim in f-string below)
    QUESTIONS_PER_ATTEMPT = questions_per_attempt  # noqa: F841
    TIMER_MINUTES = timer_minutes                  # noqa: F841

    accent, accent2 = ACCENT_COLORS.get(module_id, ("#60a5fa", "#3b82f6"))
    tags = DOMAIN_TAGS.get(module_id, [module_name])
    storage_pass = f"cca_{module_id.replace('-', '_')}_pass_count"
    storage_wrongs = f"cca_{module_id.replace('-', '_')}_wrong_answers"

    bank_json = json.dumps(bank, ensure_ascii=False, indent=2)
    tags_json = json.dumps(tags, ensure_ascii=False)
    module_name_json = json.dumps(module_name, ensure_ascii=False)

    # CSS code span uses accent color
    code_bg = accent.replace("#", "") if accent.startswith("#") else accent
    # Build rgba for code bg and option selection
    # We'll just embed the colors directly

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CCA - {module_name} Quiz</title>
<style>
  :root {{
    --bg: #09090b;
    --surface: #10101a;
    --surface2: #17172200;
    --surface3: #1e1e2c;
    --border: #252535;
    --border2: #2e2e42;
    --text: #e4e4f0;
    --text2: #a8a8c0;
    --text3: #7878a0;
    --accent: {accent};
    --accent2: {accent2};
    --green: #4ade80;
    --red: #fb7185;
    --amber: #fbbf24;
    --radius: 13px;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 1.5rem 1rem 2rem;
  }}
  code {{
    font-family: ui-monospace, 'Cascadia Code', 'Fira Mono', monospace;
    background: rgba(96,165,250,0.12);
    color: #93c5fd;
    padding: 0.1em 0.38em;
    border-radius: 5px;
    font-size: 0.855em;
    border: 1px solid rgba(96,165,250,0.2);
  }}
  .container {{ width: 100%; max-width: 780px; }}
  .card {{
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: var(--radius);
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 28px rgba(0,0,0,0.4), 0 1px 3px rgba(0,0,0,0.3);
  }}
  .card h2 {{ font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }}
  .card p {{ color: var(--text2); margin-bottom: 1rem; line-height: 1.7; }}

  .progress-wrap {{ margin-bottom: 1.5rem; }}
  .progress-bar {{ height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }}
  .progress-fill {{ height: 100%; background: linear-gradient(90deg, var(--accent2), var(--accent)); transition: width 0.35s ease; border-radius: 2px; }}

  .pass-tracker {{ display: flex; gap: 0.5rem; justify-content: center; margin-bottom: 1.5rem; }}
  .pass-dot {{ width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--border); transition: all 0.3s ease; }}
  .pass-dot.earned {{ background: var(--green); border-color: var(--green); box-shadow: 0 0 12px rgba(74,222,128,0.4); }}
  .pass-dot.current {{ border-color: var(--accent); animation: pulse 1.5s infinite; }}
  @keyframes pulse {{ 0%,100% {{ box-shadow: 0 0 0 0 rgba(96,165,250,0.4); }} 50% {{ box-shadow: 0 0 0 8px rgba(96,165,250,0); }} }}

  .domain-tags {{ display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; margin-bottom: 1.6rem; }}
  .domain-tag {{ font-size: 0.78rem; padding: 0.3rem 0.75rem; background: var(--surface2); border: 1px solid var(--border); border-radius: 999px; color: var(--text2); }}

  .start-stats {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 0.9rem; margin-bottom: 1.3rem; }}
  .stat {{ text-align: left; border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem; background: var(--surface2); }}
  .stat-value {{ font-size: 1.75rem; font-weight: 700; color: var(--accent); line-height: 1.1; }}
  .stat-label {{ font-size: 0.7rem; color: var(--text3); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.3rem; }}

  .timer {{ font-size: 0.85rem; font-variant-numeric: tabular-nums; text-align: right; margin-bottom: 0.5rem; color: var(--text2); }}
  .timer.warning {{ color: var(--amber); }}
  .timer.danger {{ color: var(--red); }}

  .quiz-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }}
  .quiz-top .progress-wrap {{ flex: 1; margin: 0; }}
  .timer-wrap {{ text-align: center; min-width: 90px; margin-left: 1rem; }}

  .q-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }}
  .q-num {{ font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent); }}
  .q-source {{ font-size: 0.75rem; color: var(--text3); background: var(--surface2); padding: 0.2rem 0.55rem; border-radius: 4px; }}
  .q-prompt {{ font-size: 1.1rem; font-weight: 500; color: #fff; margin-bottom: 1.25rem; line-height: 1.65; }}

  .options {{ display: flex; flex-direction: column; gap: 0.65rem; }}
  .option {{
    display: flex; align-items: flex-start; gap: 0.75rem;
    padding: 1rem 1.15rem; background: var(--surface2); border: 1px solid var(--border);
    border-radius: var(--radius); cursor: pointer; transition: all 0.15s ease; font-size: 1rem;
  }}
  .option:hover {{ border-color: rgba(96,165,250,0.5); background: var(--surface3); }}
  .option.selected {{ border-color: var(--accent); background: rgba(59,130,246,0.12); }}
  .option.correct {{ border-color: var(--green); background: rgba(74,222,128,0.1); }}
  .option.wrong {{ border-color: var(--red); background: rgba(251,113,133,0.1); }}
  .option.revealed-correct {{ border-color: var(--green); opacity: 0.7; }}
  .option.disabled {{ pointer-events: none; }}
  .option.disabled.selected {{ opacity: 1; }}
  .option .letter {{
    width: 1.6rem; height: 1.6rem; display: flex; align-items: center; justify-content: center;
    background: var(--border); border-radius: 6px; font-size: 0.8rem; font-weight: 700; flex-shrink: 0;
  }}
  .option.selected .letter {{ background: var(--accent); color: #fff; }}
  .option.correct .letter {{ background: var(--green); color: #000; }}
  .option.wrong .letter {{ background: var(--red); color: #fff; }}
  .option.revealed-correct .letter {{ background: var(--green); color: #000; }}

  .explanation {{
    margin-top: 1.25rem; padding: 1.25rem; background: var(--surface2); border-radius: var(--radius);
    border-left: 3px solid var(--border); font-size: 0.9rem; color: var(--text2); line-height: 1.7;
    display: none;
  }}
  .explanation.show {{ display: block; }}
  .explanation strong {{ color: #fff; }}

  .actions {{ display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; gap: 1rem; }}
  .btn {{
    padding: 0.65rem 1.5rem; border-radius: var(--radius); border: none;
    font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.15s ease;
  }}
  .btn:disabled {{ opacity: 0.35; cursor: not-allowed; }}
  .btn-primary {{ background: var(--accent2); color: #fff; }}
  .btn-primary:hover:not(:disabled) {{ filter: brightness(1.15); }}
  .btn-secondary {{ background: var(--surface2); color: var(--text); border: 1px solid var(--border); }}
  .btn-secondary:hover:not(:disabled) {{ border-color: var(--accent2); }}
  .btn-outline {{ background: transparent; color: var(--text3); border: 1px solid var(--border); font-size: 0.75rem; padding: 0.4rem 0.8rem; }}

  .question-nav {{ display: flex; justify-content: center; gap: 0.4rem; flex-wrap: wrap; margin-top: 1rem; }}
  .qnav-dot {{
    width: 36px; height: 36px; border-radius: 8px; border: 1px solid var(--border);
    background: var(--surface2); color: var(--text3); font-size: 0.9rem; cursor: pointer;
    display: flex; align-items: center; justify-content: center; transition: all 0.15s ease;
  }}
  .qnav-dot.active {{ border-color: var(--accent); background: var(--accent); color: #fff; font-weight: 700; }}
  .qnav-dot.answered-correct {{ border-color: var(--green); color: var(--green); }}
  .qnav-dot.answered-wrong {{ border-color: var(--red); color: var(--red); }}
  .qnav-dot.answered-correct.active {{ border-color: var(--green); background: var(--green); color: #fff; }}
  .qnav-dot.answered-wrong.active {{ border-color: var(--red); background: var(--red); color: #fff; }}

  .result-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem; text-align: center; }}
  .result-score {{ font-size: 4rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1; }}
  .result-score.pass {{ color: var(--green); }}
  .result-score.fail {{ color: var(--red); }}
  .result-label {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text3); margin-bottom: 0.5rem; }}
  .result-detail {{ color: var(--text3); font-size: 0.9rem; margin-top: 0.5rem; }}
  .result-detail span {{ color: #fff; font-weight: 600; }}

  .pass-summary {{ display: flex; gap: 1rem; justify-content: center; margin: 1.5rem 0; }}
  .pass-square {{
    width: 56px; height: 56px; border-radius: var(--radius); border: 2px solid var(--border);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 700; transition: all 0.3s ease;
  }}
  .pass-square.cleared {{ border-color: var(--green); background: rgba(74,222,128,0.1); color: var(--green); }}

  .review-list {{ margin-top: 1.5rem; text-align: left; max-height: 400px; overflow-y: auto; }}
  .review-item {{
    padding: 0.65rem 1rem; background: var(--surface2); border-radius: 6px;
    margin-bottom: 0.4rem; font-size: 0.825rem; display: flex; align-items: center; gap: 0.5rem;
  }}
  .review-item .rf {{ font-size: 0.65rem; flex-shrink: 0; font-weight: 700; letter-spacing: 0.08em; border-radius: 99px; padding: 0.15rem 0.5rem; border: 1px solid var(--border); }}
  .review-item .rf-ok {{ border-color: var(--green); color: var(--green); }}
  .review-item .rf-bad {{ border-color: var(--red); color: var(--red); }}

  .topic-breakdown {{ margin-top: 1.25rem; text-align: left; }}
  .topic-breakdown h3 {{ font-size: 0.85rem; color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.65rem; }}
  .topic-item {{ display: grid; grid-template-columns: 1fr auto; gap: 0.75rem; align-items: center; padding: 0.55rem 0.8rem; border: 1px solid var(--border); border-radius: 6px; margin-bottom: 0.4rem; font-size: 0.82rem; background: var(--surface2); }}
  .topic-item .topic-score {{ font-variant-numeric: tabular-nums; color: var(--text3); }}
  .topic-item .topic-score strong {{ color: #fff; }}

  .keyboard-hint {{ margin-top: 1rem; font-size: 0.75rem; color: var(--text3); text-align: center; }}
  .keyboard-hint kbd {{ font-family: inherit; border: 1px solid var(--border); border-radius: 4px; padding: 0.05rem 0.35rem; background: var(--surface2); color: var(--text2); }}

  .celebration {{ display: inline-block; margin-bottom: 0.8rem; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.22rem 0.65rem; border-radius: 999px; border: 1px solid var(--green); color: var(--green); background: rgba(74,222,128,0.12); }}

  .start-actions {{ text-align: center; }}
  .start-actions .btn {{ min-width: 280px; font-size: 1.15rem; padding: 0.9rem 2rem; border-radius: 14px; }}
  .pass-inline {{ display:flex; align-items:center; justify-content:center; gap:0.7rem; color:var(--text3); margin-bottom: 0.9rem; font-size: 0.95rem; }}
  .pass-inline .pass-tracker {{ margin: 0; }}

  @media (max-width: 600px) {{
    .start-stats {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
    .start-actions .btn {{ min-width: 0; width: 100%; }}
    .q-source {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="container" id="app">
  <div style="text-align:center;padding:3rem;color:var(--text3)">Loading quiz...</div>
</div>
<script>
(function() {{
'use strict';

var BANK = {bank_json};

var MODULE_NAME = {module_name_json};
var TAGS = {tags_json};
var PASS_STORAGE_KEY = '{storage_pass}';
var WRONGS_STORAGE_KEY = '{storage_wrongs}';
var QUESTIONS_PER_ATTEMPT = {QUESTIONS_PER_ATTEMPT};
var TIMER_MINUTES = {TIMER_MINUTES};
var PASS_SCORE = {PASS_SCORE};

function loadPassCount() {{
  try {{
    var raw = window.localStorage.getItem(PASS_STORAGE_KEY);
    var parsed = parseInt(raw, 10);
    if (Number.isFinite(parsed) && parsed >= 0) return parsed;
  }} catch (err) {{}}
  return 0;
}}

function savePassCount(n) {{
  try {{ window.localStorage.setItem(PASS_STORAGE_KEY, String(n)); }} catch (err) {{}}
}}

function loadWrongs() {{
  try {{
    var raw = window.localStorage.getItem(WRONGS_STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  }} catch (err) {{}}
  return [];
}}

function saveWrongs(arr) {{
  try {{ window.localStorage.setItem(WRONGS_STORAGE_KEY, JSON.stringify(arr)); }} catch (err) {{}}
}}

function clearWrongs() {{
  try {{ window.localStorage.removeItem(WRONGS_STORAGE_KEY); }} catch (err) {{}}
}}

var S = {{
  screen: 'start',
  pool: [],
  ix: 0,
  answers: {{}},
  revealed: false,
  timeLeft: TIMER_MINUTES * 60,
  timerId: null,
  score: null,
  review: [],
  passCount: loadPassCount(),
  warnedTwoMin: false
}};

function shuffle(a) {{
  var b = a.slice();
  for (var i = b.length - 1; i > 0; i--) {{
    var j = Math.floor(Math.random() * (i + 1));
    var t = b[i]; b[i] = b[j]; b[j] = t;
  }}
  return b;
}}

function fmtTime(s) {{
  var m = Math.floor(s / 60);
  var sec = s % 60;
  return m + ':' + (sec < 10 ? '0' : '') + sec;
}}

function shuffleOpts(q) {{
  var indices = [0,1,2,3];
  var shuffled = shuffle(indices);
  // shuffled[newIdx] = origIdx  →  origToNew[origIdx] = newIdx
  var origToNew = {{}};
  for (var ni = 0; ni < shuffled.length; ni++) origToNew[shuffled[ni]] = ni;
  return {{
    opts: shuffled.map(function(i) {{ return q.opts[i]; }}),
    correctIdx: shuffled.indexOf(q.ans),
    origToNew: origToNew
  }};
}}

function buildDeck() {{
  var picked = shuffle(BANK).slice(0, QUESTIONS_PER_ATTEMPT);
  return picked.map(function(q) {{
    var so = shuffleOpts(q);
    return {{
      source: q.source,
      prompt: q.prompt,
      opts: so.opts,
      correctIdx: so.correctIdx,
      origToNew: so.origToNew,
      expl: q.expl
    }};
  }});
}}

function startQuiz() {{
  S.screen = 'quiz';
  S.pool = buildDeck();
  S.ix = 0;
  S.answers = {{}};
  S.revealed = false;
  S.score = null;
  S.review = [];
  S.timeLeft = TIMER_MINUTES * 60;
  S.warnedTwoMin = false;
  if (S.timerId) clearInterval(S.timerId);
  S.timerId = setInterval(function() {{
    S.timeLeft--;
    if (S.timeLeft === 120 && !S.warnedTwoMin) {{
      S.warnedTwoMin = true;
      window.alert('2 minutes remaining. Any unanswered questions will be marked incorrect at 0:00.');
    }}
    if (S.timeLeft <= 0) finishQuiz();
    render();
  }}, 1000);
  render();
}}

function select(optIdx) {{
  if (S.revealed) return;
  S.answers[S.ix] = optIdx;
  S.revealed = true;
  render();
}}

function goNext() {{
  if (S.ix < S.pool.length - 1) {{
    S.ix++;
    S.revealed = S.answers[S.ix] !== undefined;
  }}
  else {{ finishQuiz(); }}
  render();
}}

function goPrev() {{
  if (S.ix > 0) {{
    S.ix--;
    S.revealed = S.answers[S.ix] !== undefined;
    render();
  }}
}}

function goTo(idx) {{
  S.ix = idx;
  S.revealed = S.answers[idx] !== undefined;
  render();
}}

function finishQuiz() {{
  if (S.timerId) clearInterval(S.timerId);
  var correct = 0;
  S.review = [];
  var wrongs = loadWrongs();
  S.pool.forEach(function(q, i) {{
    var sel = S.answers[i];
    var isCorrect = sel === q.correctIdx;
    if (isCorrect) correct++;
    S.review.push({{ q: q, selected: sel, isCorrect: isCorrect }});
    if (!isCorrect && sel !== undefined) {{
      wrongs.push({{
        source: q.source,
        prompt: q.prompt,
        selected: sel,
        correct: q.correctIdx,
        timestamp: Date.now()
      }});
    }}
  }});
  saveWrongs(wrongs);
  S.score = Math.round((correct / S.pool.length) * 1000);
  if (S.score >= PASS_SCORE) {{
    S.passCount++;
    savePassCount(S.passCount);
  }}
  S.screen = 'results';
  render();
}}

function restart() {{
  if (S.timerId) clearInterval(S.timerId);
  S = {{
    screen: 'start', pool: [], ix: 0, answers: {{}}, revealed: false,
    timeLeft: TIMER_MINUTES * 60, timerId: null, score: null, review: [], passCount: 0, warnedTwoMin: false
  }};
  savePassCount(0);
  render();
}}

function render() {{
  var app = document.getElementById('app');
  if (S.screen === 'start') app.innerHTML = renderStart();
  else if (S.screen === 'quiz') app.innerHTML = renderQuiz();
  else if (S.screen === 'results') app.innerHTML = renderResults();
}}

function letters() {{ return ['A','B','C','D']; }}

function escapeHtml(s) {{
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}}

// Inline markdown: escape HTML, render backtick code spans, bold, and newlines
function md(s) {{
  return escapeHtml(String(s))
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/[*][*]([^*]+)[*][*]/g, '<strong>$1</strong>')
    .replace(/\\n\\n/g, '<br><br>')
    .replace(/\\n/g, '<br>');
}}

function relabelSegment(seg, origToNew) {{
  return seg.replace(/^([A-D])\s+(is\s+(?:wrong|incorrect))/i, function(_, letter, rest) {{
    var origIdx = letter.toUpperCase().charCodeAt(0) - 65;
    var newIdx = origToNew[origIdx];
    return letters()[newIdx] + ' ' + rest;
  }});
}}

function buildVerboseExplanation(q, answered) {{
  var correctIdx = q.correctIdx;
  var correctLetter = letters()[correctIdx];
  var selectedLetter = answered >= 0 ? letters()[answered] : '-';
  var isCorrect = answered === correctIdx;

  var raw = q.expl || 'No explanation provided.';
  var segments = raw
    .replace(/\.\s+([A-D])\s+is\s+(wrong|incorrect)/gi, '.\\n$1 is $2')
    .replace(/\.\s+Option\s+([A-D])\b/gi, '.\\nOption $1')
    .split('\\n')
    .map(function(s) {{ return s.trim(); }})
    .filter(Boolean);

  if (q.origToNew) {{
    segments = segments.map(function(seg, i) {{
      return i === 0 ? seg : relabelSegment(seg, q.origToNew);
    }});
    // Sort wrong-option segments A→B→C→D by their remapped leading letter
    var first = segments[0];
    var rest = segments.slice(1).sort(function(a, b) {{
      var la = a.match(/^([A-D])\s+is/i); var lb = b.match(/^([A-D])\s+is/i);
      if (!la || !lb) return 0;
      return la[1].toUpperCase().charCodeAt(0) - lb[1].toUpperCase().charCodeAt(0);
    }});
    segments = [first].concat(rest);
  }}

  var segHTML = '';
  for (var si = 0; si < segments.length; si++) {{
    if (si === 0) {{
      segHTML += '<div style="margin-top:0.6rem">' + md(segments[si]) + '</div>';
    }} else {{
      segHTML += '<div style="margin-top:0.55rem;border-top:1px solid rgba(255,255,255,0.07);padding-top:0.5rem">' + md(segments[si]) + '</div>';
    }}
  }}

  return (
    '<div class="explanation show" style="border-left-color:' + (isCorrect ? 'var(--green)' : 'var(--red)') + '">' +
      '<strong>' + (isCorrect ? 'Correct' : 'Incorrect') + ' — Correct answer: ' + correctLetter + '</strong><br>' +
      (isCorrect
        ? '<span style="color:var(--green);font-weight:600">Your answer: ' + selectedLetter + '.</span>'
        : '<span style="color:var(--red);font-weight:600">Your answer: ' + selectedLetter + '.</span>') +
      segHTML +
    '</div>'
  );
}}

function renderStart() {{
  return '<div class="card start-main" style="text-align:center">' +
    '<h2>CCA — ' + escapeHtml(MODULE_NAME) + '</h2>' +
    '<p>' + BANK.length + '-question bank. Each attempt randomly selects <strong>' + QUESTIONS_PER_ATTEMPT + '</strong> questions with <strong>shuffled answer orders</strong>.<br>Pass = <strong>' + PASS_SCORE + '/1000</strong> (perfect). You must pass <strong>2 times</strong>.</p>' +
    '<div class="pass-tracker" id="passTracker">' +
      [1,2].map(function(n) {{
        return '<div class="pass-dot' + (n <= S.passCount ? ' earned' : '') + (n === S.passCount + 1 ? ' current' : '') + '"></div>';
      }}).join('') +
    '</div>' +
    (S.passCount >= 2 ? '<p style="color:var(--green);font-weight:700;margin-bottom:1rem">Module pass requirement complete: 2 perfect passes achieved.</p>' : '') +
    '<div class="domain-tags">' + TAGS.map(function(t) {{ return '<span class="domain-tag">' + escapeHtml(t) + '</span>'; }}).join('') + '</div>' +
    '<div class="start-stats">' +
      '<div class="stat"><div class="stat-value">' + BANK.length + '</div><div class="stat-label">Question Bank</div></div>' +
      '<div class="stat"><div class="stat-value">' + QUESTIONS_PER_ATTEMPT + '</div><div class="stat-label">Per Test</div></div>' +
      '<div class="stat"><div class="stat-value">' + TIMER_MINUTES + '</div><div class="stat-label">Minutes</div></div>' +
      '<div class="stat"><div class="stat-value">' + PASS_SCORE + '/1000</div><div class="stat-label">Pass Score</div></div>' +
    '</div>' +
    '<p style="font-size:0.8rem;color:var(--text3);margin-bottom:1.5rem">Pass policy: ' + QUESTIONS_PER_ATTEMPT + ' questions per attempt, perfect score required, two successful runs needed.</p>' +
    '<div class="start-actions"><button class="btn btn-primary" id="btnStart">Start Quiz (' + QUESTIONS_PER_ATTEMPT + ' Questions)</button></div>' +
    '<p style="font-size:0.8rem;color:var(--text3);margin-top:0.95rem">Progress is saved in this browser until you reset it.</p>' +
  '</div>';
}}

function renderQuiz() {{
  var q = S.pool[S.ix];
  var answered = S.answers[S.ix] !== undefined ? S.answers[S.ix] : -1;
  var progress = ((S.ix + (answered >= 0 ? 1 : 0)) / S.pool.length) * 100;
  var tc = S.timeLeft < 120 ? 'danger' : S.timeLeft < 300 ? 'warning' : '';

  var optHTML = '';
  for (var i = 0; i < q.opts.length; i++) {{
    var cls = 'option';
    if (answered === i) cls += ' selected';
    if (S.revealed) {{
      cls += ' disabled';
      if (i === q.correctIdx) cls += answered === i ? ' correct' : ' revealed-correct';
      else if (answered === i) cls += ' wrong';
    }}
    optHTML += '<div class="' + cls + '" data-opt="' + i + '"><span class="letter">' + letters()[i] + '</span><span>' + md(q.opts[i]) + '</span></div>';
  }}

  var expHTML = '';
  if (S.revealed) {{
    expHTML = buildVerboseExplanation(q, answered);
  }}

  return (
    '<div class="quiz-top">' +
      '<div class="progress-wrap"><div class="progress-bar"><div class="progress-fill" style="width:' + progress + '%"></div></div></div>' +
      '<div class="timer-wrap"><div class="timer ' + tc + '">' + fmtTime(S.timeLeft) + '</div></div>' +
    '</div>' +
    '<div class="card quiz-card">' +
      '<div class="q-header"><span class="q-num">Q ' + (S.ix + 1) + ' / ' + S.pool.length + '</span><span class="q-source">' + escapeHtml(q.source) + '</span></div>' +
      '<div class="q-prompt">' + md(q.prompt) + '</div>' +
      '<div class="options" id="optGroup">' + optHTML + '</div>' +
      expHTML +
      '<div class="actions">' +
        '<button class="btn btn-secondary" id="btnPrev"' + (S.ix === 0 ? ' disabled' : '') + '>Previous</button>' +
        '<span>' + (S.revealed ? '<button class="btn btn-primary" id="btnNext">' + (S.ix === S.pool.length - 1 ? 'See Results' : 'Next') + '</button>' : '<span style="color:var(--text3);font-size:0.92rem">Select an answer to reveal feedback</span>') + '</span>' +
      '</div>' +
      '<div class="keyboard-hint"><kbd>1-4</kbd> answer <kbd>Enter</kbd> next <kbd>Left/Right</kbd> navigate</div>' +
    '</div>' +
    '<div class="question-nav" id="qNav">' +
      S.pool.map(function(_, i) {{
        var cls2 = 'qnav-dot';
        if (i === S.ix) cls2 += ' active';
        if (S.answers[i] !== undefined) cls2 += S.answers[i] === S.pool[i].correctIdx ? ' answered-correct' : ' answered-wrong';
        return '<div class="' + cls2 + '" data-idx="' + i + '">' + (i + 1) + '</div>';
      }}).join('') +
    '</div>'
  );
}}

function renderResults() {{
  var s = S.score;
  var passed = s >= PASS_SCORE;
  var correctN = 0;
  for (var i = 0; i < S.review.length; i++) {{ if (S.review[i].isCorrect) correctN++; }}

  var reviewHTML = '';
  for (var i2 = 0; i2 < S.review.length; i2++) {{
    var r = S.review[i2];
    reviewHTML += '<div class="review-item"' + (r.isCorrect ? ' style="border-left:3px solid var(--green);background:rgba(74,222,128,0.05);"' : ' style="border-left:3px solid var(--red);background:rgba(251,113,133,0.06);"') + '><span class="rf ' + (r.isCorrect ? 'rf-ok">OK' : 'rf-bad">MISS') + '</span><span><strong>Q' + (i2 + 1) + ':</strong> ' + (r.isCorrect ? 'Correct' : 'Picked ' + (r.selected >= 0 ? letters()[r.selected] : '-') + ', answer was ' + letters()[r.q.correctIdx]) + ' — ' + escapeHtml(r.q.source) + '</span></div>';
  }}

  var passHTML = '';
  for (var n = 1; n <= 2; n++) {{
    passHTML += '<div class="pass-square' + (n <= S.passCount ? ' cleared' : '') + '">' + (n <= S.passCount ? 'OK' : n) + '</div>';
  }}

  var bySource = {{}};
  for (var j = 0; j < S.review.length; j++) {{
    var src = S.review[j].q.source;
    if (!bySource[src]) bySource[src] = {{ total: 0, correct: 0 }};
    bySource[src].total++;
    if (S.review[j].isCorrect) bySource[src].correct++;
  }}
  var sourceRows = Object.keys(bySource).sort(function(a, b) {{
    var aRate = bySource[a].correct / bySource[a].total;
    var bRate = bySource[b].correct / bySource[b].total;
    return aRate - bRate;
  }}).map(function(src2) {{
    var item = bySource[src2];
    return '<div class="topic-item"><span>' + escapeHtml(src2) + '</span><span class="topic-score"><strong>' + item.correct + '</strong> / ' + item.total + '</span></div>';
  }}).join('');

  var weakHTML = '';
  var allWrongs = loadWrongs();
  if (allWrongs.length > 0) {{
    var wrongsBySource = {{}};
    allWrongs.forEach(function(w) {{
      if (!wrongsBySource[w.source]) wrongsBySource[w.source] = [];
      wrongsBySource[w.source].push(w);
    }});
    var sortedSources = Object.keys(wrongsBySource).sort(function(a, b) {{
      return wrongsBySource[b].length - wrongsBySource[a].length;
    }});
    weakHTML = '<div class="topic-breakdown"><h3>Weak Areas (' + allWrongs.length + ' total misses)</h3>';
    sortedSources.forEach(function(src3) {{
      var items = wrongsBySource[src3];
      weakHTML += '<div style="margin-bottom:0.8rem"><div class="topic-item"><span>' + escapeHtml(src3) + '</span><span class="topic-score"><strong>' + items.length + '</strong> miss' + (items.length > 1 ? 'es' : '') + '</span></div>';
      var seen = {{}};
      items.forEach(function(w) {{
        var key = w.prompt.substring(0, 60);
        if (!seen[key]) seen[key] = 0;
        seen[key]++;
      }});
      Object.keys(seen).forEach(function(k) {{
        weakHTML += '<div style="font-size:0.75rem;color:var(--text3);padding:0.2rem 0.8rem;margin-left:0.5rem;border-left:2px solid var(--border)">Missed ' + seen[k] + 'x: ' + escapeHtml(k) + '…</div>';
      }});
      weakHTML += '</div>';
    }});
    weakHTML += '</div>';
  }}

  return (
    '<div class="result-card">' +
      (passed && S.passCount >= 2
        ? '<div class="celebration">Playbook Complete</div><p style="color:var(--green);font-size:1.25rem;font-weight:700">All 2 perfect passes complete.</p>'
        : passed
          ? '<div class="celebration">Perfect Pass</div><p style="color:var(--green);font-size:1.1rem;font-weight:700">Perfect this run. ' + (2 - S.passCount) + ' more perfect run' + (2 - S.passCount > 1 ? 's' : '') + ' required.</p>'
          : '<p style="color:var(--red);font-size:1rem;font-weight:700;margin-bottom:0.6rem">Below threshold. Retake immediately after reviewing misses.</p>') +
      '<div class="result-label">Your Score</div>' +
      '<div class="result-score ' + (passed ? 'pass' : 'fail') + '">' + s + '<span style="font-size:1.5rem">/1000</span></div>' +
      '<div class="result-detail"><span>' + correctN + '</span> of <span>' + S.pool.length + '</span> correct <span>' + (passed ? 'PASS' : 'RETEST') + '</span></div>' +
      '<div class="pass-summary">' + passHTML + '</div>' +
      '<div class="topic-breakdown"><h3>Topic Breakdown</h3>' + sourceRows + '</div>' +
      weakHTML +
      '<div class="review-list">' + reviewHTML + '</div>' +
      '<div style="margin-top:1.5rem;display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap">' +
        '<button class="btn btn-primary" id="btnRetry">Retake (New Shuffled Set)</button>' +
        '<button class="btn btn-secondary" id="btnReview">Review Answers</button>' +
        '<button class="btn btn-outline" id="btnReset">Reset Progress</button>' +
        (allWrongs.length > 0 ? '<button class="btn btn-outline" id="btnClearWrongs" style="border-color:var(--amber);color:var(--amber)">Clear Weak Areas</button>' : '') +
      '</div>' +
    '</div>'
  );
}}

document.getElementById('app').addEventListener('click', function(e) {{
  var t = e.target;
  if (t.id === 'btnStart') startQuiz();
  if (t.closest) {{
    var opt = t.closest('.option');
    if (opt && !S.revealed) {{
      select(parseInt(opt.getAttribute('data-opt'), 10));
    }}
  }}
  if (t.id === 'btnNext') goNext();
  if (t.id === 'btnPrev') goPrev();
  if (t.closest) {{
    var dot = t.closest('.qnav-dot');
    if (dot) goTo(parseInt(dot.getAttribute('data-idx'), 10));
  }}
  if (t.id === 'btnRetry') startQuiz();
  if (t.id === 'btnReview') {{
    S.screen = 'quiz'; S.ix = 0; S.revealed = true;
    for (var k = 0; k < S.pool.length; k++) {{
      if (S.answers[k] === undefined) S.answers[k] = S.review[k].selected;
    }}
    render();
  }}
  if (t.id === 'btnReset') restart();
  if (t.id === 'btnClearWrongs') {{
    clearWrongs();
    render();
  }}
}});

document.addEventListener('keydown', function(e) {{
  if (S.screen !== 'quiz') return;
  if (e.key.length === 1 && ((e.key >= '1' && e.key <= '4') || (e.key >= 'a' && e.key <= 'd') || (e.key >= 'A' && e.key <= 'D'))) {{
    var idx = -1;
    if (e.key >= '1' && e.key <= '4') idx = parseInt(e.key, 10) - 1;
    else idx = e.key.toUpperCase().charCodeAt(0) - 65;
    if (idx >= 0 && idx <= 3 && !S.revealed) {{
      select(idx);
      e.preventDefault();
    }}
  }}
  if (e.key === 'Enter') {{
    if (S.revealed) goNext();
    e.preventDefault();
  }}
  if (e.key === 'ArrowLeft') {{
    goPrev();
    e.preventDefault();
  }}
  if (e.key === 'ArrowRight') {{
    if (S.revealed) goNext();
    e.preventDefault();
  }}
}});

render();
}})();
</script>
</body>
</html>"""


def generate_module(module: dict, output_dir: Path) -> Path:
    module_id = module["id"]
    module_name = module["name"]
    bank_path = ROOT / module["path"]

    if not bank_path.exists():
        raise FileNotFoundError(f"Module bank not found: {bank_path}")

    questions = parse_markdown(bank_path, module_name)
    if not questions:
        raise ValueError(f"No questions parsed from {bank_path}")

    print(f"  {module_id}: parsed {len(questions)} questions")

    qpa = module.get("questions_per_attempt", min(QUESTIONS_PER_ATTEMPT, len(questions)))
    tm = module.get("timer_minutes", TIMER_MINUTES)
    html = generate_html(module_id, module_name, questions, questions_per_attempt=qpa, timer_minutes=tm)

    output_file = output_dir / f"cca-{module_id}-quiz.html"
    output_file.write_text(html, encoding="utf-8")
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate self-contained HTML quiz files from module bank Markdown files."
    )
    parser.add_argument(
        "--module",
        default=None,
        help="Single module/concept ID to generate (e.g. ci-cd, hooks). Omit to generate all.",
    )
    parser.add_argument(
        "--output-dir",
        default="quizzes",
        help="Output directory for HTML files (default: quizzes).",
    )
    parser.add_argument(
        "--concepts-only",
        action="store_true",
        help="Generate only concept quizzes (agentic-loops, mcp, tool-use, hooks).",
    )
    parser.add_argument(
        "--modules-only",
        action="store_true",
        help="Generate only the 6 scenario module quizzes.",
    )
    args = parser.parse_args()

    if not MANIFEST_PATH.exists():
        sys.exit(f"Module manifest not found: {MANIFEST_PATH}. Run tools/build_module_banks.py first.")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    scenario_modules = manifest["modules"]
    all_modules = scenario_modules + CONCEPT_MODULES
    by_id = {m["id"]: m for m in all_modules}

    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.module:
        if args.module not in by_id:
            sys.exit(f"Unknown module id: {args.module!r}. Available: {', '.join(by_id)}")
        targets = [by_id[args.module]]
    elif args.concepts_only:
        targets = CONCEPT_MODULES
    elif args.modules_only:
        targets = scenario_modules
    else:
        targets = all_modules

    print(f"Generating {len(targets)} quiz file(s) -> {output_dir}")
    created = []
    for module in targets:
        try:
            out = generate_module(module, output_dir)
            created.append(out)
            print(f"  -> {out}")
        except Exception as exc:
            print(f"  ERROR [{module['id']}]: {exc}", file=sys.stderr)

    print(f"\nDone. {len(created)} file(s) created.")
    for f in created:
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
