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
   - `docs/quiz-generation/QUIZ-GENERATION-FLOW.md`
3. Run the timed quiz block (CLI date test or the HTML quiz flow).

### B) When pass criteria is achieved
1. Keep normal quiz logs (automatic for CLI via `logs/cca_quiz_attempts.jsonl`).
2. For HTML/manual passes, append explicit checkpoint event:
   - `./cca record-pass --date YYYY-MM-DD --method html --topic <topic> --quiz-file quizzes/cca-<topic>-quiz.html --score 1000 --perfect-run-count 2`
3. Verify persistence:
   - `tail -n 5 logs/cca_pass_events.jsonl`

## Recent Fixes and Pitfalls

Moved to the dated log below - this section stays short by design. Fold a
fact here only once it's durable enough to read every session.

## Obsidian Integration Notes
- Vault created at `/Users/thinh/Documents/Obsidian/Operator-HQ`.
- CCA lane note: `/Users/thinh/Documents/Obsidian/Operator-HQ/02-Lanes/CCA-Cert/CCA-6Week-Execution.md`.
- Obsidian CLI exists at `/Users/thinh/.local/bin/obsidian-cli` but desktop setting `Command line interface` must be enabled in Obsidian app.

## Next-Pass Update Rule
- Keep the curated sections above append-only in spirit, but small: fold in a
  fact only once it holds up as durable.
- Add a dated entry under `docs/agent-memory/deltas/<year-month>.md` after
  each meaningful study-system/tooling change - not under this heading, and
  not under "Recent Fixes and Pitfalls" above (that section is retired).
- Do not rewrite old dated entries; add clarifications as new dated bullets.

## Dated history

All prior dated entries (2026-05-08 through 2026-07-08, both from "Recent
Fixes and Pitfalls" and the ones that had accumulated under "Next-Pass Update
Rule" instead of following its own instruction) moved to
`docs/agent-memory/deltas/2026-05.md` and `docs/agent-memory/deltas/2026-07.md`
as part of adopting the two-tier memory convention (see the global `AGENTS.md`'s
"Project Memory" section for why). Nothing was deleted - read those files for
full history.
