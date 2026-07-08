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

## Playbook Actions (Reading Complete + Pass Complete)
### A) When reading is complete for a topic/day
1. Confirm today's scope:
   - `./cca read --date YYYY-MM-DD`
2. Generate or refresh the topic HTML quiz artifact (for example `quizzes/cca-hooks-quiz.html`) using:
   - `tools/QUIZ-GENERATION-FLOW.md`
3. Run the timed quiz block (CLI date test or the HTML quiz flow).

### B) When pass criteria is achieved
1. Keep normal quiz logs (automatic for CLI via `logs/cca_quiz_attempts.jsonl`).
2. For HTML/manual passes, append explicit checkpoint event:
   - `./cca record-pass --date YYYY-MM-DD --method html --topic <topic> --quiz-file quizzes/cca-<topic>-quiz.html --score 1000 --perfect-run-count 2`
3. Verify persistence:
   - `tail -n 5 logs/cca_pass_events.jsonl`

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
- Tuned `quizzes/cca-tool-use-quiz.html` with persisted pass tracking via `localStorage` (`cca_domain1_pass_count`) so 3-perfect-run progress survives page reloads.
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
- Created `quizzes/cca-agentic-loops-quiz.html`: 10-question HTML quiz for Domain 1.1 (Agentic Loops) matching Tool Use quiz format. Uses teal accent, same pass tracking + wrong answer tracking pattern. localStorage keys: `cca_agentic_loops_pass_count`, `cca_agentic_loops_wrong_answers`.
- Created Obsidian domain note: `03-Knowledge/CCA-Domains/domain-1.md` — condensed decision rules + anti-patterns for all 15 Domain 1 topics. Later expanded with Agentic Loops control flow, conversation history management, and error handling sections.
- Created Obsidian daily note: `02-Lanes/CCA-Cert/Daily/2026-05-09.md`.

### 2026-05-10
- Expanded `quizzes/cca-agentic-loops-quiz.html` from 10 to 30 questions (20 per attempt, matching Tool Use quiz format).
- Fixed ambiguous question with near-duplicate options on display: "omitted" question in Agentic Loops quiz.
- Domain 1.1 (Agentic Loops) completed: 2/2 perfect passes.
- Changed all HTML quiz timers from 90 minutes to 15 minutes (with 2-minute warning).
- Created Obsidian daily note: `02-Lanes/CCA-Cert/Daily/2026-05-10.md`.
- Created `tools/QUIZ-GENERATION-FLOW.md` — standardized process for generating HTML quizzes from practice-test markdown banks.
- Fetched all MCP docs (intro, architecture, build-server, build-client, debugging, apps).
- Created Obsidian domain note: `03-Knowledge/CCA-Domains/domain-2.md` — MCP Integration with metaphors (USB-C, Restaurant), architecture, transports, lifecycle, debugging, MCP apps vs web apps, glossary (uv, stdio, absolute paths).
- Created `quizzes/cca-mcp-quiz.html` — 30-question HTML quiz for Domain 2 (MCP Integration) with amber accent, 15min timer, 2 perfect passes. localStorage keys: `cca_mcp_pass_count`, `cca_mcp_wrong_answers`. Topics: architecture, primitives, transports, lifecycle, debugging, MCP apps, configuration, client patterns, security.

## Obsidian Integration Notes
- Vault created at `/Users/thinh/Documents/Obsidian/Operator-HQ`.
- CCA lane note: `/Users/thinh/Documents/Obsidian/Operator-HQ/02-Lanes/CCA-Cert/CCA-6Week-Execution.md`.
- Obsidian CLI exists at `/Users/thinh/.local/bin/obsidian-cli` but desktop setting `Command line interface` must be enabled in Obsidian app.

## Next-Pass Update Rule
- Keep this file append-only.
- Add a dated entry under `Recent Fixes and Pitfalls` after each meaningful study-system/tooling change.
- Do not rewrite old entries; add clarifications as new dated bullets.

### 2026-07-08
- Added two shareable standalone prep-guide HTML files for a colleague:
  - `docs/prep-guides/cca-f-what-it-tests.html` — Diataxis explanation/reference page covering exam format, target candidate, scenarios, domain weights, and excluded topics.
  - `docs/prep-guides/cca-f-how-to-prepare.html` — Diataxis how-to page covering official guide first, Academy courses, exam-guide exercises, practice exam readiness, community resources, and final booking checks.
- Browser-render QA covered desktop `1440x1200` and mobile `390x1200`; both pages had no horizontal overflow.
- Refreshed the `cca-f-how-to-prepare.html` resource section with `last30days` + GitHub API checks for CCA-F repositories. Added primary, targeted, and extra-drill repo tiers plus a caution against dump-style repos.

### 2026-05-10
- Accelerated schedule update after Week 1 completed in 2 days: moved Week 2 start to 2026-05-11 by shifting upcoming plan one week earlier for 2026-05-11..2026-06-12.
- Added 2026-06-13..2026-06-19 as optional buffer/retest window (full sim + weak-area corrections).
- Regenerated calendar/cca_6week_plan.md from calendar/cca_daily_plan.json to keep CLI plan and human table aligned.

### 2026-05-16
- Processed user transcript-based hooks confusion into structured study artifacts:
  - Obsidian daily note: `/Users/thinh/Documents/Obsidian/Operator-HQ/02-Lanes/CCA-Cert/Daily/2026-05-16.md`
  - Obsidian hooks deep-dive note: `/Users/thinh/Documents/Obsidian/Operator-HQ/03-Knowledge/CCA-Domains/domain-1-hooks-deep-dive.md`
  - Added backlink from `domain-1.md` to hooks deep-dive companion.
- Added repo quiz artifact `quizzes/cca-hooks-quiz.md` with 30 scenario-based hook questions + answer key covering lifecycle, matcher/if filters, decision control, async constraints, HTTP/MCP hook behavior, and managed-hook policy controls.
- Calendar checkpoint: module-order schedule from 2026-05-16 21:00 onward remained aligned with `Module 1/7 -> Module 7/7` sequence.

### 2026-05-16 (Post-Finish Quiz Playbook)
- Executed post-quiz completion flow after user finished hooks quiz:
  - Updated Obsidian daily note in active vault:
    - `/Users/thinh/Documents/Obsidian/CCA-Study/01-Daily/2026-05-16.md`
  - Updated hooks sprint checklist:
    - `/Users/thinh/Documents/Obsidian/CCA-Study/02-Lanes/Domain-1-Hooks-Sprint.md`
  - Updated lane status/review notes:
    - `/Users/thinh/Documents/Obsidian/CCA-Study/02-Lanes/Domain-1-Tool-Use.md`
- Recorded playbook completion state for hooks quiz as user-confirmed finish with perfect-pass policy:
  - `20 questions per attempt`
  - `1000/1000 required`
  - `2 successful perfect runs`
- Note: `qmd` lookup in this repo was unstable (`SQLITE_BUSY_RECOVERY` and Bun crash), so direct file reads were used as fallback for playbook execution.

### 2026-05-17
- Added explicit playbook actions for two operator checkpoints:
  - finish-reading -> generate/refresh HTML quiz artifact
  - pass-complete -> persist checkpoint event in repo log
- Added CLI command `./cca record-pass` to write append-only pass events to:
  - `logs/cca_pass_events.jsonl`
- Updated CLI docs + quiz generation flow docs to include the checkpoint command so future sessions can recover exact progress from logs.

### 2026-05-17 (Exam Debrief + Real Question Analysis)
- Completed grill-me debrief after first practice test attempt. Key findings:
  - 60 questions, 90 min (1.5 min/question). 4 of 6 scenarios randomly selected.
  - Finished with 30-40 min buffer. Skimming early hurt scores; careful reading improved.
  - 5-6 point difficulty gap between current practice tests and real exam.
  - Questions are more verbose, constraint-dense, cross-domain within a single scenario.
  - Distractors are same length, no gimmicks, negated by specific constraints in the question.
  - Exam is hands-on, not theoretical — requires exact syntax (field names, config paths, flags).
  - All 4 failure mode categories tested (tool, context, API, model behavior).
- Wrote full debrief to `docs/exam-debrief-1.md`.
- Updated `PREPARATION-GUIDE.md` with Quiz Question Construction Patterns based on real exam analysis.
- Stored 15 real exam questions from Scenario 1 (Code Generation with Claude Code) at `practice-tests/real-exam-questions/scenario-01-code-generation.md`.
- Dominant theme discovered: **context management via configuration** — 7 of 15 questions (47%) revolve around "load the right context at the right time."
  - `context: fork` appeared as answer in 3 questions
  - Skills on-demand loading in 2 questions
  - `.claude/rules/` glob patterns for conditional loading in 1 question
  - Explore subagent for isolation in 1 question
- New patterns for quiz generation added to playbook:
  - Multi-symptom config questions (match frontmatter to symptoms)
  - Context pollution questions (right isolation mechanism)
  - On-demand vs always-loaded context questions (CLAUDE.md vs Skills vs .claude/rules/)
  - Config location questions (project vs user scope)
  - Concrete examples as the fix for prose ambiguity
  - Skill customization without affecting team (different name in ~/.claude/skills/)
- Distractor design rules codified: similar length, no gimmicks, plausible but flawed, constraint-negated, mixes scoping levels, prompt-based as common wrong answer
- Explanation rules codified: why correct, why each distractor wrong, principle at work
- Scenario 2 (Multi-Agent Research System) analyzed:
  - 15 questions stored at `practice-tests/real-exam-questions/scenario-02-multi-agent-research.md`
  - Dominant theme: error propagation & architecture (33% of questions)
  - New patterns: error taxonomy distinction, coverage annotations, least privilege via tool interface, scoped capabilities, tool naming ambiguity, structured output over verbose content, task partitioning before delegation, local recovery before escalation
  - Cross-scenario comparison: Each scenario has distinct "gravitational pull." Scenario 1 = config-driven context management. Scenario 2 = error propagation & architecture.
   - Playbook extended with 8 new patterns (patterns 8-15) covering multi-agent domain
- Scenario 3 (Claude Code for CI/CD) analyzed:
  - 15 questions stored at `practice-tests/real-exam-questions/scenario-03-ci-cd.md`
  - Dominant theme: batch vs sync API decisions (27%) + prompt engineering for consistency (20%)
  - New patterns: batch API technical incompatibility, FP trust cascading, inline reasoning for triage, prior findings as context, CLI flags (`-p`, `--output-format json`, `--json-schema`)
  - Playbook extended with 5 new patterns (patterns 16-20) covering CI/CD domain
  - Three-scenario map: S1=config/context (47%), S2=error/architecture (33%), S3=API decisions/prompt (27%+20%)
- Scenario 4 (Customer Support Agent) analyzed:
  - 15 questions stored at practice-tests/real-exam-questions/scenario-04-customer-support.md
  - Dominant theme: tool selection reliability (27%) + escalation decisions (13%)
  - User got Q5 and Q9 wrong — critical few-shot vs self-critique/preprocessing traps documented
  - New patterns: persistent case facts block, keyword-sensitive prompt diagnosis, parallel decomposition with shared context, user disambiguation over heuristics, tool batching via prompt
  - Playbook extended with 8 new patterns (patterns 21-28) covering customer support domain
  - Four-scenario map complete

### 2026-05-17 (Scenario-Pattern Refactor After First Pass)
- Replaced domain-silo daily calendar with scenario-pattern blocks in `calendar/cca_daily_plan.json` using ordered priority:
  1) context isolation, 2) error propagation, 3) batch vs sync, 4) tool selection, 5) config scope, 6) prompt boundaries.
- Added 10 weekday anti-pattern drills (30 minutes each) directly into reading blocks.
- Added dedicated few-shot decision-boundary blocks (few-shot vs self-critique vs preprocessing) on 2026-06-12, 2026-06-16, and 2026-06-18.
- Added 4 full-scenario timed exams (15Q, 22m) on 2026-05-23, 2026-05-30, 2026-06-06, 2026-06-13 and verified `./cca test --date ...` execution.
- Regenerated `calendar/cca_6week_plan.md` from the JSON and added `calendar/cca_refactored_rationale.md` documenting all structural changes.
- Coverage check now explicitly spans all 6 canonical scenarios each week via artifact mapping in reading/test_sources.

### 2026-05-17 (Prep-Style Exam Generator + 30Q Module Banks)
- Added module bank builder: `tools/build_module_banks.py`.
  - Output location: `practice-tests/module-banks/`.
  - Generates 6 scenario modules at 30 questions each plus `manifest.json`.
- Added single-file prep exam generator: `tools/cca_generate_exam_html.py`.
  - Default output: `quizzes/cca-prep-exam.html`.
  - Default format: 60Q / 90m from 4 modules x 15 questions.
  - Supports stable rotation with `--seed`, explicit module pinning with repeated `--module-id`.
- Added CLI command: `./cca exam-html` in `tools/cca.py`.
  - Example: `./cca exam-html --seed 20260523 --modules 4 --per-module 15 --timed-minutes 90 --output quizzes/cca-prep-exam-2026-05-23.html`
- Updated exam-day schedule commands in `calendar/cca_daily_plan.json` to use `./cca exam-html ...` so each timed exam is prep-test structured and emitted as one HTML file.
- Regenerated plan views: `calendar/cca_6week_plan.md` and `calendar/cca_6week_plan-md`.

### 2026-05-17 (Weekday Learning Plan + Small-Quiz Standard)
- Refined all remaining weekday entries (2026-05-18 onward) in `calendar/cca_daily_plan.json` with explicit `weekday_learning_objective` per day.
- Standardized weekday quiz runs to small format:
  - `./cca test --date YYYY-MM-DD --count 8 --timed-minutes 20`
- Embedded per-day quiz standard contract via `small_quiz_standard` and reading checklist references to:
  - `PREPARATION-GUIDE.md` -> Distractor Design Rules + Explanation Rules
- Added weekday-only view:
  - `calendar/cca_weekday_learning_plan.md`
- Regenerated plan render files:
  - `calendar/cca_6week_plan.md`
  - `calendar/cca_6week_plan-md`
