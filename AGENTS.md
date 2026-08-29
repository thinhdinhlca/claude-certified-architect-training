# Claude Certified Architect — AGENTS.md

> Global rules: `~/AGENTS.md` applies to every agent session on this machine regardless of repo. This file adds only project-specific context — do not duplicate or weaken the global rules.

## Project overview

A personal 12-week study workspace for the Claude Certified Architect – Foundations (CCA-F) exam: a curriculum in `README.md`, Python CLI tooling for daily reading/testing, generated practice-test banks and HTML quizzes, a JSON-driven calendar plan, and an optional companion Obsidian vault outside this repo (`/Users/thinh/Documents/Obsidian/...`). There is no package.json — this is a plain Python 3 project, no build step.

## Commands

- `./cca list` — show everything the workspace can do.
- `./cca read --date YYYY-MM-DD` — show today's reading.
- `./cca test --date YYYY-MM-DD [--count N] [--timed-minutes N] [--seed N]` — interactive graded quiz.
- `./cca sim --seed N` — full 60-question/120-minute mock exam.
- `./cca exam-html --seed N --modules N --per-module N --timed-minutes N --output <path>` — generate a standalone HTML prep exam.
- `./cca record-pass --date YYYY-MM-DD --method html --topic <topic> --quiz-file <path> --score N --perfect-run-count N` — persist an HTML/manual pass checkpoint.
- `./cca stats --last N` — score trend.
- Full command reference: `docs/cli.md` (progressive disclosure).

## Where facts live

One fact lives in exactly one file. If two files could hold it, pick the row below and edit only that file.

| Kind of fact | File |
|---|---|
| Domain glossary, architecture map, known hotspots, startup/playbook protocol, dated fixes (append-only) | `docs/agent-memory.md` |
| Base curriculum, anti-patterns, decision frameworks | `README.md` |
| Full CLI reference | `docs/cli.md` |
| Quiz question construction patterns | `docs/PREPARATION-GUIDE.md` |
| Real-exam debrief and analysis | `docs/exam-debrief-1.md` |
| Gamified progression layer | `GAME.md` |
| Canonical date-indexed schedule | `calendar/cca_daily_plan.json` |
| Question banks | `practice-tests/` |

Do not create a new top-level `*.md` knowledge or context file. Add the fact to the file above that already owns its category, or add a new row to this table in the same edit if none fits.

This is enforced, not just documented: `.githooks/pre-commit` blocks a commit that adds a new top-level `*.md` file this table (or `AGENTS.md` generally) doesn't name. A fresh clone must run `git config core.hooksPath .githooks` once before it takes effect.

## Boundaries

- `docs/agent-memory.md` is explicitly append-only per its own "Next-Pass Update Rule" — add dated bullets, don't rewrite old entries.
- This repo has real uncommitted work in progress (calendar/plan edits, quiz HTML drafts) — do not discard it.
