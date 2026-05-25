#!/usr/bin/env python3
"""
rebuild_scenario_html.py

Parses module bank .md files from practice-tests/module-banks/ and replaces the
SCENARIOS JavaScript constant in quizzes/cca-scenario-exam.html.
"""

import re
import json
import os

# Scenario metadata in order
SCENARIO_META = [
    {"id": "code-generation",       "name": "Code Generation with Claude Code",    "accent": "#4f8cff", "accentRgb": "79,140,255"},
    {"id": "multi-agent-research",  "name": "Multi-Agent Research",                "accent": "#2dd4bf", "accentRgb": "45,212,191"},
    {"id": "ci-cd",                 "name": "CI/CD with Claude Code",              "accent": "#f59e0b", "accentRgb": "245,158,11"},
    {"id": "customer-support",      "name": "Customer Support Automation",         "accent": "#a78bfa", "accentRgb": "167,139,250"},
    {"id": "developer-productivity","name": "Developer Productivity",              "accent": "#4ade80", "accentRgb": "74,222,128"},
    {"id": "structured-extraction", "name": "Structured Data Extraction",          "accent": "#fb7185", "accentRgb": "251,113,133"},
]

# Filename to scenario id mapping
FILE_TO_SCENARIO = {
    "module-code-generation.md":       "code-generation",
    "module-multi-agent-research.md":  "multi-agent-research",
    "module-ci-cd.md":                 "ci-cd",
    "module-customer-support.md":      "customer-support",
    "module-developer-productivity.md":"developer-productivity",
    "module-structured-extraction.md": "structured-extraction",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANKS_DIR = os.path.join(ROOT, "practice-tests", "module-banks")
HTML_PATH = os.path.join(ROOT, "quizzes", "cca-scenario-exam.html")


def parse_module_bank(filepath):
    """Parse a module bank .md file and return list of question dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on ## Question N boundaries
    # Each chunk starts with the question text after the header
    question_blocks = re.split(r'^## Question \d+\s*$', content, flags=re.MULTILINE)

    # First chunk is the file header — skip it
    question_blocks = question_blocks[1:]

    questions = []
    for block in question_blocks:
        block = block.strip()
        if not block:
            continue

        # Split into main body and details section
        # <details> block contains the answer
        details_match = re.search(
            r'<details><summary>Answer</summary>(.*?)</details>',
            block,
            re.DOTALL | re.IGNORECASE
        )
        if not details_match:
            print(f"  WARNING: no <details> block found in block starting: {block[:60]!r}")
            continue

        details_content = details_match.group(1).strip()
        main_body = block[:details_match.start()].strip()

        # --- Parse options from main_body ---
        # Find option lines A) B) C) D)
        opt_pattern = re.compile(r'^([A-D])\)\s+(.+)', re.MULTILINE)
        opt_matches = list(opt_pattern.finditer(main_body))
        if len(opt_matches) != 4:
            print(f"  WARNING: expected 4 options, found {len(opt_matches)} in: {main_body[:80]!r}")
            continue

        # Prompt is everything before the first option
        prompt_text = main_body[:opt_matches[0].start()].strip()

        # Build opts list in order A B C D
        opts = [m.group(2).strip() for m in opt_matches]

        # --- Parse answer from details ---
        # Format: **X)** explanation text (source: ...)
        answer_match = re.match(r'\*\*([A-D])\)\*\*\s*(.*)', details_content, re.DOTALL)
        if not answer_match:
            print(f"  WARNING: could not parse answer from details: {details_content[:80]!r}")
            continue

        answer_letter = answer_match.group(1)
        answer_idx = ord(answer_letter) - ord('A')

        explanation_raw = answer_match.group(2).strip()

        # Strip (source: ...) at the end — it may be after a newline or inline
        explanation = re.sub(r'\s*\(source:[^)]*\)\s*$', '', explanation_raw, flags=re.DOTALL).strip()

        # Collapse internal newlines in explanation to single space for cleaner JS
        explanation = re.sub(r'\s*\n\s*', ' ', explanation).strip()
        prompt_text = re.sub(r'\s*\n\s*', ' ', prompt_text).strip()

        questions.append({
            "prompt": prompt_text,
            "opts": opts,
            "answerIdx": answer_idx,
            "explanation": explanation,
        })

    return questions


def build_scenarios_js(scenarios_data):
    """Build the JavaScript SCENARIOS constant string."""
    lines = ["const SCENARIOS = ["]
    for i, scenario in enumerate(scenarios_data):
        is_last = (i == len(scenarios_data) - 1)
        meta = scenario["meta"]
        questions = scenario["questions"]

        q_parts = []
        for q in questions:
            q_js = (
                "{prompt:" + json.dumps(q["prompt"], ensure_ascii=False) +
                ",opts:" + json.dumps(q["opts"], ensure_ascii=False) +
                ",answerIdx:" + str(q["answerIdx"]) +
                ",explanation:" + json.dumps(q["explanation"], ensure_ascii=False) +
                "}"
            )
            q_parts.append(q_js)

        questions_js = "[" + ",".join(q_parts) + "]"

        scenario_js = (
            "  {id:" + json.dumps(meta["id"]) +
            ",name:" + json.dumps(meta["name"]) +
            ",accent:" + json.dumps(meta["accent"]) +
            ",accentRgb:" + json.dumps(meta["accentRgb"]) +
            ",questions:" + questions_js +
            "}" +
            ("" if is_last else ",")
        )
        lines.append(scenario_js)

    lines.append("];")
    return "\n".join(lines)


def main():
    # 1. Parse all module banks
    scenarios_data = []
    for meta in SCENARIO_META:
        scenario_id = meta["id"]
        # Find the filename that maps to this scenario id
        filename = None
        for fn, sid in FILE_TO_SCENARIO.items():
            if sid == scenario_id:
                filename = fn
                break
        if filename is None:
            raise ValueError(f"No filename mapping for scenario id: {scenario_id}")

        filepath = os.path.join(BANKS_DIR, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Module bank not found: {filepath}")

        print(f"Parsing {filename}...")
        questions = parse_module_bank(filepath)
        print(f"  -> {len(questions)} questions parsed")

        scenarios_data.append({"meta": meta, "questions": questions})

    # 2. Build the new SCENARIOS JS
    new_scenarios_js = build_scenarios_js(scenarios_data)

    # 3. Read the HTML file
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 4. Find the SCENARIOS constant in the HTML
    # The constant starts with "const SCENARIOS = [" on a line
    # and ends with "];" on that same line (it's all on one line in the current file)
    # or on a subsequent line. We'll handle both cases.
    #
    # Strategy: find the line(s) from "const SCENARIOS = [" to the closing "];"
    # We'll use a line-based approach.
    lines = html_content.split('\n')

    start_line_idx = None
    end_line_idx = None

    for idx, line in enumerate(lines):
        if 'const SCENARIOS = [' in line and start_line_idx is None:
            start_line_idx = idx
            # Check if it also ends on this line
            # Count brackets to find the matching ]
            # For the single-line case: ends with ]};  or ];
            # We need to find where the array closes
            # Simple approach: if the line itself contains the closing ]; after the opening
            break

    if start_line_idx is None:
        raise ValueError("Could not find 'const SCENARIOS = [' in the HTML file")

    # Now find the end: scan from start_line_idx, track bracket depth
    bracket_depth = 0
    found_start = False
    for idx in range(start_line_idx, len(lines)):
        line = lines[idx]
        for char in line:
            if char == '[':
                bracket_depth += 1
                found_start = True
            elif char == ']':
                bracket_depth -= 1
                if found_start and bracket_depth == 0:
                    end_line_idx = idx
                    break
        if end_line_idx is not None:
            break

    if end_line_idx is None:
        raise ValueError("Could not find the closing ]; for SCENARIOS")

    print(f"\nFound SCENARIOS on lines {start_line_idx + 1}–{end_line_idx + 1}")

    # Detect the indentation of the start line
    start_line = lines[start_line_idx]
    indent = len(start_line) - len(start_line.lstrip())
    indent_str = start_line[:indent]

    # Indent the new JS to match
    new_lines = new_scenarios_js.split('\n')
    indented_new = '\n'.join(indent_str + l if l else l for l in new_lines)

    # Replace the lines
    new_html_lines = lines[:start_line_idx] + [indented_new] + lines[end_line_idx + 1:]
    new_html_content = '\n'.join(new_html_lines)

    # 5. Write back
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html_content)

    print(f"\nSuccessfully updated {HTML_PATH}")

    # 6. Quick verification
    total_q = sum(len(s["questions"]) for s in scenarios_data)
    print(f"Total questions written: {total_q} (expected 180)")


if __name__ == "__main__":
    main()
