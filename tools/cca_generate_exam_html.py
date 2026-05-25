#!/usr/bin/env python3
"""Generate a single self-contained prep-style exam HTML.

Default format matches final exam shape:
- 180 questions total
- 6 modules (all available)
- 30 questions per module
- 150-minute timer
"""

from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "practice-tests" / "module-banks" / "manifest.json"


@dataclass
class Question:
    qid: str
    module_id: str
    module_name: str
    prompt: str
    options: list[str]
    answer_idx: int
    explanation: str
    source: str


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_markdown(path: Path, module_id: str, module_name: str) -> list[Question]:
    text = path.read_text(encoding="utf-8")
    heading_regex = re.compile(r"^(## Question \d+|### Q\d+)\s*$", re.M)
    matches = list(heading_regex.finditer(text))
    rows: list[Question] = []

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

        details = re.search(r"<details>.*?<summary>Answer</summary>(.*?)</details>", block, flags=re.S)
        explanation = norm(re.sub(r"<.*?>", " ", details.group(1))) if details else ""

        qn = re.search(r"(\d+)", m.group(1))
        n = qn.group(1) if qn else str(idx + 1)

        rows.append(
            Question(
                qid=f"{path.stem}:{n}",
                module_id=module_id,
                module_name=module_name,
                prompt=prompt,
                options=options,
                answer_idx=answer_idx,
                explanation=explanation,
                source=str(path.relative_to(ROOT)),
            )
        )

    return rows


def load_modules() -> list[dict]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Module manifest not found: {MANIFEST_PATH}. Run tools/build_module_banks.py first.")
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return data["modules"]


def build_exam(selected_modules: list[dict], per_module: int, seed: int | None) -> tuple[list[Question], int]:
    rng = random.Random(seed)
    picked: list[Question] = []

    for m in selected_modules:
        bank_path = ROOT / m["path"]
        questions = parse_markdown(bank_path, m["id"], m["name"])
        if len(questions) < per_module:
            raise SystemExit(
                f"Module '{m['id']}' has {len(questions)} questions but {per_module} required."
            )
        picked.extend(rng.sample(questions, per_module))

    rng.shuffle(picked)
    return picked, rng.randint(0, 999999)


def emit_html(questions: list[Question], selected_modules: list[dict], output: Path, timed_minutes: int, seed: int | None) -> None:
    payload = [
        {
            "id": q.qid,
            "moduleId": q.module_id,
            "moduleName": q.module_name,
            "prompt": q.prompt,
            "opts": q.options,
            "answerIdx": q.answer_idx,
            "explanation": q.explanation,
            "source": q.source,
        }
        for q in questions
    ]
    modules_meta = [{"id": m["id"], "name": m["name"]} for m in selected_modules]
    generated_at = datetime.now().isoformat(timespec="seconds")

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>CCA Prep Exam ({len(questions)}Q)</title>
  <style>
    :root {{ --bg:#0b1020; --card:#121a2e; --text:#e8edf7; --muted:#9fb0d1; --accent:#4f8cff; --good:#1bbf76; --bad:#ef5350; --border:#22304d; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; background:linear-gradient(180deg,#0b1020,#0a0f1d); color:var(--text); font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial; }}
    .wrap {{ max-width:960px; margin:0 auto; padding:24px; }}
    .card {{ background:var(--card); border:1px solid var(--border); border-radius:14px; padding:18px; }}
    .meta {{ color:var(--muted); font-size:13px; line-height:1.5; }}
    .title {{ margin:0 0 8px; font-size:24px; }}
    .row {{ display:flex; gap:12px; flex-wrap:wrap; align-items:center; }}
    .pill {{ font-size:12px; color:#cfe0ff; border:1px solid #2e4677; padding:4px 8px; border-radius:999px; }}
    .btn {{ background:var(--accent); color:white; border:none; border-radius:10px; padding:10px 14px; font-weight:600; cursor:pointer; }}
    .btn.alt {{ background:#1a243b; border:1px solid var(--border); }}
    .qtext {{ font-size:17px; line-height:1.5; margin:10px 0 14px; }}
    .opt {{ border:1px solid var(--border); border-radius:10px; padding:10px 12px; margin:8px 0; cursor:pointer; }}
    .opt:hover {{ border-color:#3f5f9a; }}
    .opt.sel {{ border-color:#6da1ff; background:#122140; }}
    .opt.good {{ border-color:var(--good); background:#112c20; }}
    .opt.bad {{ border-color:var(--bad); background:#3a1a21; }}
    .ex {{ margin-top:12px; border-left:3px solid #355da8; padding:8px 10px; color:#d8e3ff; background:#101a31; border-radius:8px; font-size:14px; line-height:1.45; }}
    .small {{ color:var(--muted); font-size:12px; }}
    .hidden {{ display:none; }}
    .score {{ font-size:28px; font-weight:700; margin:8px 0; }}
    code {{ font-family:ui-monospace,monospace; background:rgba(79,140,255,0.12); color:#a5c4ff; padding:0.1em 0.38em; border-radius:4px; font-size:0.855em; }}
  </style>
</head>
<body>
  <div class=\"wrap\" id=\"app\"></div>
  <script>
  const BANK = {json.dumps(payload, ensure_ascii=False)};
  const MODULES = {json.dumps(modules_meta, ensure_ascii=False)};
  const META = {{
    generatedAt: {json.dumps(generated_at)},
    timedMinutes: {timed_minutes},
    totalQuestions: BANK.length,
    perModule: BANK.length / MODULES.length,
    seed: {json.dumps(seed)}
  }};

  const S = {{ ix:0, answers:Array(BANK.length).fill(-1), revealed:false, timer:null, left:META.timedMinutes*60, done:false }};

  function esc(s) {{ return String(s).replace(/[&<>\"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}}[c])); }}
  function mdInline(s) {{
    return esc(s)
      .replace(/[*][*](.+?)[*][*]/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\\n\\n/g, '<br><br>')
      .replace(/\\n/g, '<br>');
  }}
  function letter(i) {{ return ['A','B','C','D'][i] || '?'; }}
  function fmt(sec) {{ const m=Math.floor(sec/60), s=sec%60; return String(m).padStart(2,'0')+':'+String(s).padStart(2,'0'); }}

  function renderStart() {{
    const mods = MODULES.map(m => `<span class=\"pill\">${{esc(m.name)}}</span>`).join(' ');
    return `
      <div class=\"card\">
        <h1 class=\"title\">CCA Prep-Style Exam</h1>
        <div class=\"meta\">${{META.totalQuestions}} questions, ${{META.timedMinutes}} minutes, ${{MODULES.length}} modules, ${{META.perModule}} questions per module.</div>
        <div class=\"meta\">Generated: ${{esc(META.generatedAt)}} | seed: ${{META.seed ?? 'random'}}</div>
        <div style=\"margin-top:10px\" class=\"row\">${{mods}}</div>
        <div style=\"margin-top:14px\"><button class=\"btn\" onclick=\"startExam()\">Start Exam</button></div>
      </div>`;
  }}

  function renderExam() {{
    const q = BANK[S.ix];
    const selected = S.answers[S.ix];
    let opts = '';
    for (let i=0;i<4;i++) {{
      let cls = 'opt';
      if (selected === i) cls += ' sel';
      if (S.revealed) {{
        if (i === q.answerIdx) cls += ' good';
        else if (selected === i) cls += ' bad';
      }}
      opts += `<div class=\"${{cls}}\" onclick=\"pick(${{i}})\"><strong>${{letter(i)}})</strong> ${{mdInline(q.opts[i])}}</div>`;
    }}

    const ex = S.revealed ? `<div class=\"ex\"><strong>Explanation:</strong> ${{mdInline(q.explanation || 'No explanation provided.')}}</div>` : '';

    return `
      <div class=\"card\">
        <div class=\"row\" style=\"justify-content:space-between\">
          <div class=\"small\">Q ${{S.ix+1}} / ${{BANK.length}} · ${{esc(q.moduleName)}}</div>
          <div><strong>${{fmt(S.left)}}</strong></div>
        </div>
        <div class=\"qtext\">${{esc(q.prompt)}}</div>
        ${{opts}}
        ${{ex}}
        <div class=\"row\" style=\"margin-top:12px\">
          <button class=\"btn alt\" onclick=\"prevQ()\" ${{S.ix===0?'disabled':''}}>Prev</button>
          <button class=\"btn\" onclick=\"revealOrNext()\">${{S.revealed ? (S.ix===BANK.length-1?'Finish':'Next') : 'Check'}}</button>
          <button class=\"btn alt\" onclick=\"finishExam()\">Finish Now</button>
        </div>
      </div>`;
  }}

  function renderResult() {{
    let correct=0;
    for (let i=0;i<BANK.length;i++) if (S.answers[i] === BANK[i].answerIdx) correct++;
    const score = Math.round((correct / BANK.length) * 1000);
    const pass = score >= 720;
    const byMod = {{}};
    for (const q of BANK) byMod[q.moduleName] = byMod[q.moduleName] || {{t:0,c:0}};
    for (let i=0;i<BANK.length;i++) {{
      const m = byMod[BANK[i].moduleName];
      m.t += 1;
      if (S.answers[i] === BANK[i].answerIdx) m.c += 1;
    }}
    const rows = Object.entries(byMod).map(([k,v]) => `<div class=\"small\">${{esc(k)}}: ${{v.c}}/${{v.t}}</div>`).join('');

    return `
      <div class=\"card\">
        <h2 style=\"margin:0\">Exam Complete</h2>
        <div class=\"score\">${{score}} / 1000</div>
        <div class=\"meta\">Correct: ${{correct}} / ${{BANK.length}} · Result: <strong>${{pass ? 'PASS' : 'RETEST'}}</strong></div>
        <div style=\"margin-top:10px\">${{rows}}</div>
        <div class=\"row\" style=\"margin-top:14px\"><button class=\"btn\" onclick=\"location.reload()\">Generate New Run</button></div>
      </div>`;
  }}

  function mount() {{
    const app = document.getElementById('app');
    if (!S.done && !S.timer) app.innerHTML = renderStart();
    else if (!S.done) app.innerHTML = renderExam();
    else app.innerHTML = renderResult();
  }}

  function startExam() {{
    S.timer = setInterval(() => {{
      S.left--;
      if (S.left <= 0) finishExam();
      else mount();
    }}, 1000);
    mount();
  }}

  function pick(i) {{ if (S.done || S.revealed) return; S.answers[S.ix] = i; mount(); }}
  function prevQ() {{ if (S.done || S.ix === 0) return; S.revealed = false; S.ix--; mount(); }}
  function revealOrNext() {{
    if (S.done) return;
    if (!S.revealed) {{ if (S.answers[S.ix] < 0) return; S.revealed = true; mount(); return; }}
    if (S.ix >= BANK.length - 1) {{ finishExam(); return; }}
    S.ix++; S.revealed = false; mount();
  }}

  function finishExam() {{
    if (S.done) return;
    S.done = true;
    if (S.timer) clearInterval(S.timer);
    mount();
  }}

  mount();
  </script>
</body>
</html>
"""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a single prep-style CCA exam HTML")
    parser.add_argument("--output", default="quizzes/cca-prep-exam.html", help="Output HTML path")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--modules", type=int, default=6, help="Number of modules to sample")
    parser.add_argument("--per-module", type=int, default=30, help="Questions per selected module")
    parser.add_argument("--timed-minutes", type=int, default=150, help="Timer in minutes")
    parser.add_argument(
        "--all-modules",
        action="store_true",
        default=False,
        help="Select all available modules regardless of --modules count (future-proof).",
    )
    parser.add_argument(
        "--module-id",
        action="append",
        default=[],
        help="Optional module id(s). If provided, exactly those modules are used.",
    )
    args = parser.parse_args()

    modules = load_modules()
    by_id = {m["id"]: m for m in modules}
    rng = random.Random(args.seed)

    if args.module_id:
        selected = []
        for mid in args.module_id:
            if mid not in by_id:
                raise SystemExit(f"Unknown module id: {mid}")
            selected.append(by_id[mid])
    elif args.all_modules:
        selected = list(modules)
    else:
        if args.modules > len(modules):
            raise SystemExit(f"Requested {args.modules} modules but only {len(modules)} available")
        selected = rng.sample(modules, args.modules)

    if len(selected) == 0:
        raise SystemExit("No modules selected")

    questions, _ = build_exam(selected, args.per_module, args.seed)
    total = len(questions)
    if total != len(selected) * args.per_module:
        raise SystemExit("Exam assembly mismatch")

    output = ROOT / args.output
    emit_html(questions, selected, output, args.timed_minutes, args.seed)

    print(f"Generated exam HTML: {output}")
    print(f"Modules: {', '.join(m['id'] for m in selected)}")
    print(f"Questions: {total} ({args.per_module} per module)")
    print(f"Timer: {args.timed_minutes} minutes")


if __name__ == "__main__":
    main()
