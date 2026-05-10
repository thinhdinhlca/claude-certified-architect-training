# Agent Memory (Append-Only)

## Domain Glossary
- `CCA-F`: Claude Certified Architect - Foundations exam.
- `Scaled score`: 0-1000 scoring; target pass threshold in this repo is `720`.
- `Interactive test`: CLI-driven MCQ session with immediate scoring and unlimited retakes.
- `Full simulation`: 60-question, 120-minute mock run (`--full-sim`).
- `Weekday pattern`: read `8:00-9:00 PM`, test `9:00-10:00 PM`.
- `Weekend pattern`: read `9:00-11:00 AM`, review `4:00-5:00 PM`, test `8:00-10:00 PM`.

## Architecture Map
- `README.md`: base 12-week curriculum + anti-patterns + decision frameworks.
- `GAME.md`: gamified progression layer (XP/streak/challenge framing).
- `practice-tests/`: question banks (`test-01`..`test-10`) + `full-exam-01.md`.
- `calendar/cca_daily_plan.json`: canonical date-indexed schedule and per-day test source mapping.
- `calendar/cca_6week_plan.md`: human-readable date-by-date study table with links.
- `tools/cca_today.py`: prints exact plan for a date (materials + test command).
- `tools/cca_quiz.py`: interactive test engine (timed, graded, logs attempts).
- `logs/cca_quiz_attempts.jsonl`: append-only attempt history.

## Known Hotspots
- Parsing quality depends on markdown shape in `practice-tests/*.md` (`## Question` or `### Q` headers and `A)`..`D)` options).
- `--full-sim` requires enough parsed questions in bank; if structure changes, revalidate parser output.
- Daily test source routing comes from `calendar/cca_daily_plan.json`; incorrect mapping here changes what gets tested.
- Calendar events are recurring templates; per-day specifics live in the local plan files, not in event text.

## Startup Protocol (Tomorrow Study Pass)
1. Open today plan:
   - `python3 tools/cca_today.py --date YYYY-MM-DD`
2. Finish reading materials listed in the output.
3. Run interactive test:
   - `python3 tools/cca_quiz.py --date YYYY-MM-DD`
4. If score `< 720`, retest immediately (unlimited):
   - rerun same command, optionally `--seed <n>`.
5. For exam-condition mock:
   - `python3 tools/cca_quiz.py --full-sim --seed 42`
6. Check attempt history:
   - `tail -n 5 logs/cca_quiz_attempts.jsonl`

## Recent Fixes and Pitfalls
### 2026-05-08
- Added 6-week plan artifacts (`calendar/cca_daily_plan.json`, `calendar/cca_6week_plan.md`).
- Added interactive quiz tooling (`tools/cca_quiz.py`, `tools/cca_today.py`).
- Added `.gitignore` for `.DS_Store`, `__pycache__`, and attempt logs.
- Fixed early-quit display bug in quiz scoreboard denominator.
- Created recurring Google Calendar blocks tied to these local artifacts.
- Added unified CLI launcher (`./cca` -> `tools/cca.py`) with commands: `list`, `read`, `plan`, `content`, `test`, `sim`, `stats`, `obsidian`.
- Added progressive-disclosure docs:
  - `docs/cli.md`
  - `docs/obsidian-rules.md`
- `./cca content` currently shows 150 parsable question headings across local banks.

### 2026-05-09
- Tuned `tools/cca-tool-use-quiz.html` with persisted pass tracking via `localStorage` (`cca_domain1_pass_count`) so 3-perfect-run progress survives page reloads.
- Added one-time 5-minute timer warning (`window.alert`) before auto-submit at 0:00.
- Added keyboard controls on quiz screen: `1-4`/`A-D` select options, `Enter` checks answer or advances after reveal, arrow keys navigate (`Left` previous, `Right` next after reveal).
- Added per-topic results breakdown (grouped by `source`) to identify weak areas after each run.
- Removed emoji-based status markers in results UI and replaced with text badges (`OK` / `MISS`) for cleaner, consistent rendering.
- Updated start/quiz layouts toward a brighter cyan-glass visual style (hero intro, stat tiles, breadcrumb/timer top row, larger answer cards) to match the new UI reference.
- Removed explicit `Check Answer`: selecting an option now reveals correctness + explanation immediately, then `Next` advances to the next question.
- Rewrote all 30 quiz explanations to remove hardcoded letter references (A/B/C/D) — explanations now use "The correct answer..." so they remain accurate after option shuffling.
- Balanced answer lengths across all 30 questions — correct answer no longer consistently the longest option.
- Added dynamic correct answer indicator to explanation display: shows `Correct — [letter]` or `Incorrect — [letter]` based on shuffled position.
- Changed pass threshold from 3 to 2 perfect runs to complete Domain 1.
- Added wrong answer tracking: `cca_domain1_wrong_answers` in localStorage accumulates misses across sessions. Results screen shows "Weak Areas" section grouped by topic with miss counts. Added "Clear Weak Areas" button.
- Domain 1 HTML quiz completed: 2/2 perfect passes.
- Created Obsidian domain note: `03-Knowledge/CCA-Domains/domain-1.md` — condensed decision rules + anti-patterns for all 15 Domain 1 topics.
- Created Obsidian daily note: `02-Lanes/CCA-Cert/Daily/2026-05-09.md`.
- Created `tools/cca-agentic-loops-quiz.html`: 10-question HTML quiz for Domain 1.1 (Agentic Loops) matching Tool Use quiz format. Uses teal accent, same pass tracking + wrong answer tracking pattern. localStorage keys: `cca_agentic_loops_pass_count`, `cca_agentic_loops_wrong_answers`.
- Created Obsidian domain note: `03-Knowledge/CCA-Domains/domain-1.md` — condensed decision rules + anti-patterns for all 15 Domain 1 topics. Later expanded with Agentic Loops control flow, conversation history management, and error handling sections.
- Created Obsidian daily note: `02-Lanes/CCA-Cert/Daily/2026-05-09.md`.

### 2026-05-10
- Expanded `tools/cca-agentic-loops-quiz.html` from 10 to 30 questions (20 per attempt, matching Tool Use quiz format).
- Fixed ambiguous question with near-duplicate options on display: "omitted" question in Agentic Loops quiz.
- Domain 1.1 (Agentic Loops) completed: 2/2 perfect passes.
- Changed all HTML quiz timers from 90 minutes to 15 minutes (with 2-minute warning).
- Created Obsidian daily note: `02-Lanes/CCA-Cert/Daily/2026-05-10.md`.
- Created `tools/QUIZ-GENERATION-FLOW.md` — standardized process for generating HTML quizzes from practice-test markdown banks.
- Fetched all MCP docs (intro, architecture, build-server, build-client, debugging, apps).
- Created Obsidian domain note: `03-Knowledge/CCA-Domains/domain-2.md` — MCP Integration with metaphors (USB-C, Restaurant), architecture, transports, lifecycle, debugging, MCP apps vs web apps, glossary (uv, stdio, absolute paths).
- Created `tools/cca-mcp-quiz.html` — 30-question HTML quiz for Domain 2 (MCP Integration) with amber accent, 15min timer, 2 perfect passes. localStorage keys: `cca_mcp_pass_count`, `cca_mcp_wrong_answers`. Topics: architecture, primitives, transports, lifecycle, debugging, MCP apps, configuration, client patterns, security.

## Obsidian Integration Notes
- Vault created at `/Users/thinh/Documents/Obsidian/Operator-HQ`.
- CCA lane note: `/Users/thinh/Documents/Obsidian/Operator-HQ/02-Lanes/CCA-Cert/CCA-6Week-Execution.md`.
- Obsidian CLI exists at `/Users/thinh/.local/bin/obsidian-cli` but desktop setting `Command line interface` must be enabled in Obsidian app.

## Next-Pass Update Rule
- Keep this file append-only.
- Add a dated entry under `Recent Fixes and Pitfalls` after each meaningful study-system/tooling change.
- Do not rewrite old entries; add clarifications as new dated bullets.

### 2026-05-10
- Accelerated schedule update after Week 1 completed in 2 days: moved Week 2 start to 2026-05-11 by shifting upcoming plan one week earlier for 2026-05-11..2026-06-12.
- Added 2026-06-13..2026-06-19 as optional buffer/retest window (full sim + weak-area corrections).
- Regenerated calendar/cca_6week_plan.md from calendar/cca_daily_plan.json to keep CLI plan and human table aligned.

