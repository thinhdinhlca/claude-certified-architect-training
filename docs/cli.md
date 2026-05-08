# CCA CLI (Progressive Disclosure)

## Level 1 - Use It Fast
- `./cca list` - show everything this workspace can do.
- `./cca read --date YYYY-MM-DD` - show what to read today.
- `./cca test --date YYYY-MM-DD` - start interactive quiz mode.
- `./cca sim --seed 42` - run full 60Q/120m mock exam.

<details>
<summary>Level 2 - Daily Study Flow</summary>

1. Check reading and sources:
   - `./cca read --date 2026-05-10`
2. Run your daily quiz:
   - `./cca test --date 2026-05-10 --count 20 --timed-minutes 90`
3. Retest with a different question sample:
   - `./cca test --date 2026-05-10 --count 20 --timed-minutes 90 --seed 99`
4. Check score trend:
   - `./cca stats --last 10`

</details>

<details>
<summary>Level 3 - Command Reference</summary>

### `list`
- Purpose: print capabilities and examples.
- Example: `./cca list`

### `read`
- Purpose: show one-day focus, reading checklist, test sources, and suggested test command.
- Flags:
  - `--date YYYY-MM-DD` (optional)

### `plan`
- Purpose: display a date-window slice from `calendar/cca_daily_plan.json`.
- Flags:
  - `--from-date YYYY-MM-DD`
  - `--to-date YYYY-MM-DD`
- Example:
  - `./cca plan --from-date 2026-05-09 --to-date 2026-05-16`

### `content`
- Purpose: list markdown test banks and parsed question counts.
- Example:
  - `./cca content`

### `test`
- Purpose: run interactive quiz using `tools/cca_quiz.py`.
- Flags:
  - `--date YYYY-MM-DD`
  - `--source practice-tests/test-01-agentic-loops.md` (repeatable)
  - `--count N`
  - `--timed-minutes N`
  - `--seed N`
  - `--reveal`
  - `--dry-run`

### `sim`
- Purpose: full simulation (`--full-sim` pass-through).
- Flags:
  - `--seed N`
  - `--reveal`
  - `--dry-run`

### `stats`
- Purpose: aggregate recent scores from `logs/cca_quiz_attempts.jsonl`.
- Flags:
  - `--last N` (default: 10)

### `obsidian`
- Purpose: show Obsidian rules file path and status.
- Example:
  - `./cca obsidian`

</details>

<details>
<summary>Level 4 - Troubleshooting</summary>

- `./cca` says "permission denied":
  - Run `chmod +x ./cca`.
- No entries for a date:
  - Confirm key exists in `calendar/cca_daily_plan.json`.
- `stats` looks odd:
  - Check raw logs: `tail -n 20 logs/cca_quiz_attempts.jsonl`.
- Need to inspect what `test` will run without starting quiz:
  - Use `--dry-run`.

</details>
