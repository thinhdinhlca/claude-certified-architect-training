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

## Obsidian Integration Notes
- Vault created at `/Users/thinh/Documents/Obsidian/Operator-HQ`.
- CCA lane note: `/Users/thinh/Documents/Obsidian/Operator-HQ/02-Lanes/CCA-Cert/CCA-6Week-Execution.md`.
- Obsidian CLI exists at `/Users/thinh/.local/bin/obsidian-cli` but desktop setting `Command line interface` must be enabled in Obsidian app.

## Next-Pass Update Rule
- Keep this file append-only.
- Add a dated entry under `Recent Fixes and Pitfalls` after each meaningful study-system/tooling change.
- Do not rewrite old entries; add clarifications as new dated bullets.
