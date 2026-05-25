# Scenario 1: Code Generation with Claude Code (15 Questions)

> Pasted from real exam practice attempt. Answers are real exam answers.

---

## Q1: Slack integration — multiple valid approaches, ambiguous requirements
**Correct:** A — Plan mode to explore integration options and architectural implications before implementing.
**Why it's right:** Multiple valid approaches with significantly different architectural implications + ambiguous requirements = plan mode.
**Wrongs:** Direct execution with guessing (B, C, D) is premature when requirements are unclear.

---

## Q2: API response transformation — prose requirements misinterpreted
**Correct:** D — Provide 2-3 concrete input-output examples showing expected transformation.
**Why it's right:** Concrete examples eliminate ambiguity inherent in prose. Directly addresses root cause (misinterpretation).
**Wrongs:** More prose (A, B) doesn't solve the interpretation problem. JSON schema (C) validates but doesn't guide transformation logic.

---

## Q3: GitHub MCP server — team credentials without committing secrets
**Correct:** B — Project-scoped `.mcp.json` with `${GITHUB_TOKEN}` env var expansion, document in README.
**Why it's right:** Single version-controlled source of truth + per-developer credential injection via env vars.
**Wrongs:** Placeholder token (A) requires manual override per dev. Wrapper (C) adds unnecessary complexity. User scope (D) loses team consistency.

---

## Q4: Personal skill customization without affecting teammates
**Correct:** D — Personal version in `~/.claude/skills/` with a different name (`/my-commit`).
**Why it's right:** Project skills take precedence over personal skills with same name. Different name avoids collision.
**Wrongs:** `override: true` (A) not a valid frontmatter option. Conditional logic (B) adds complexity. Same name (C) won't work.

---

## Q5: Three skill issues — missing args, context bleeding, destructive tool access
**Correct:** A — `argument-hint` + `context: fork` + `allowed-tools` restriction.
**Why it's right:** Three distinct config features address three distinct issues deterministically.
**Wrongs:** Prompt-based validation (B) is probabilistic. Splitting skills (C) doesn't solve context bleeding or tool restriction. Positional params (D) don't solve context bleeding or tool restriction.

---

## Q6: Monolithic CLAUDE.md — organizing into topic-specific modules
**Correct:** A — Create separate markdown files in `.claude/rules/` covering one topic each.
**Why it's right:** `.claude/rules/` is the designated directory for topic-specific rule organization.
**Wrongs:** `config.yaml` (B) doesn't exist. Multiple CLAUDE.md at different levels (C) is for hierarchy, not topic organization. README.md files (D) are human docs, not Claude config.

---

## Q7: Exemplar endpoints for consistency — only needed for new endpoint creation
**Correct:** A — Create a skill with exemplar code, invoked on-demand via slash command.
**Why it's right:** Ensures context is loaded only when generating new endpoints, not during unrelated tasks.
**Wrongs:** CLAUDE.md (B) loads exemplars for every task, wasting context. Manual copy (C) is error-prone. Path-specific rules (D) might load for other API directory work.

---

## Q8: Always-loaded standards vs task-specific workflows
**Correct:** C — Universal standards in CLAUDE.md, task-specific workflows as Skills.
**Why it's right:** CLAUDE.md is always loaded (coding standards, testing conventions). Skills invoked on-demand (PR review, deployment, migration).
**Wrongs:** @import (A) still loads everything always. All as skills (B) means standards aren't always loaded. Path-specific rules (D) don't address task-specific nature.

---

## Q9: Monolith to microservices restructuring
**Correct:** D — Plan mode to explore codebase, understand dependencies, design approach before implementing.
**Why it's right:** Complex, multi-file, architectural restructuring with decisions about service boundaries = plan mode.
**Wrongs:** Direct execution (A, B, C) on architectural restructuring risks costly mistakes.

---

## Q10: Different coding conventions for different file types — auto-apply by path
**Correct:** B — Rule files in `.claude/rules/` with YAML frontmatter glob patterns for conditional application.
**Why it's right:** Glob patterns (`**/*.test.tsx`, `src/api/**/*.ts`) activate rules automatically and deterministically based on file path, handling cross-cutting concerns (tests spread throughout codebase).
**Wrongs:** Root CLAUDE.md with headers (A) relies on Claude inference, not deterministic. Skills (C) require manual invocation. Separate CLAUDE.md per directory (D) doesn't solve cross-cutting test files spread throughout.

---

## Q11: Verbose analysis skill causing context pollution
**Correct:** C — Add `context: fork` to skill frontmatter.
**Why it's right:** Runs analysis in isolated sub-agent context, preventing verbose output from consuming main conversation tokens.
**Wrongs:** Model change (A) doesn't address context pollution. Output compression (B) reduces analysis quality. Splitting skills (D) doesn't solve core context problem.

---

## Q12: Custom /review command available to all developers
**Correct:** A — `.claude/commands/` in project repository.
**Why it's right:** Project-scoped commands are version-controlled and automatically available to all developers who clone/pull.
**Wrongs:** CLAUDE.md (B) is for instructions, not command definitions. `~/.claude/commands/` (C) is user-scoped, not shared. `config.json` (D) doesn't exist.

---

## Q13: Exploration skill context influencing subsequent work
**Correct:** D — Add `context: fork` to skill frontmatter.
**Why it's right:** Isolated sub-agent context prevents exploration discussion from polluting main conversation history.
**Wrongs:** Split skills (A) doesn't prevent context leakage. User-scoped (B) doesn't address the problem. Bash subprocess (C) isn't the right mechanism.

---

## Q14: New developer not receiving guideline that existing developers get
**Correct:** B — Guideline in `~/.claude/CLAUDE.md` (user-level) instead of `.claude/CLAUDE.md` (project-level). Move to project.
**Why it's right:** User-level config is not shared via version control. Project-level ensures all team members receive it. 
**Wrongs:** Per-user preference models (A) don't exist. Conflicting user-level (C) is a different scenario. Caching issues (D) aren't the root cause.

---

## Q15: Verbose API call discovery consuming context window
**Correct:** B — Use Explore subagent for Phase 1 to isolate verbose output and return summary.
**Why it's right:** Explore subagent isolates verbose discovery output in separate context, returning concise summary to main conversation.
**Wrongs:** Headless mode with `--continue` (A) breaks continuity. Batching across sessions (C) loses context for collaborative design. /compact (D) is reactive, not proactive.

---

## Question Type Summary

| Type | Count | Questions |
|------|-------|-----------|
| Plan mode vs direct execution | 2 | Q1, Q9 |
| Skills configuration (frontmatter, isolation) | 5 | Q4, Q5, Q11, Q13 |
| Skills vs CLAUDE.md (what goes where) | 2 | Q7, Q8 |
| CLAUDE.md organization (rules/, hierarchy) | 3 | Q6, Q10, Q14 |
| MCP configuration | 1 | Q3 |
| Custom commands | 1 | Q12 |
| Concrete examples / few-shot | 1 | Q2 |
| Subagent delegation (Explore) | 1 | Q15 |
| Skills customization (personal vs project) | 1 | Q4 |

## SKILL.md Frontmatter Fields Tested

| Field | Questions |
|-------|-----------|
| `context: fork` | Q5, Q11, Q13 |
| `allowed-tools` | Q5 |
| `argument-hint` | Q5 |

## Config Locations Tested

| Location | Purpose | Questions |
|----------|---------|-----------|
| `.claude/commands/` | Project-scoped custom slash commands | Q12 |
| `.claude/skills/` | Project-scoped skills | Q4, Q5, Q7, Q8 |
| `~/.claude/skills/` | Personal skills (different name) | Q4 |
| `.claude/rules/` | Topic-specific + path-scoped rules | Q6, Q10 |
| `.claude/CLAUDE.md` | Project-level always-loaded standards | Q8, Q14 |
| `~/.claude/CLAUDE.md` | User-level (not shared) | Q14 |
| `.mcp.json` | Project-scoped MCP config | Q3 |

## New Patterns NOT In Original Debrief

1. **`.claude/rules/` with YAML frontmatter glob patterns** — Path-specific conditional rule application. Solves "different conventions for different file types scattered throughout codebase." (Q10)

2. **Explore subagent** — Specific subagent type for verbose discovery tasks. Isolates output, returns summary. (Q15)

3. **Combined skill configuration** — Questions that test multiple frontmatter features simultaneously to solve a multi-symptom problem. (Q5)

4. **Skills for on-demand exemplar loading** — Exemplar code only needed for specific tasks, not always-loaded context. (Q7)

5. **Concrete examples as the answer to prose ambiguity** — When requirements are misinterpreted, concrete input-output examples beat more precise prose, JSON schemas, or asking Claude to explain itself. (Q2)

6. **MCP env var expansion** — `${GITHUB_TOKEN}` pattern for credentials without committing secrets. (Q3)

7. **Personal skill naming collision** — Project skills take precedence over personal skills with same name. Must use different name. (Q4)
