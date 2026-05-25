# Scenario 3: Claude Code for Continuous Integration (15 Questions)

> Pasted from real exam practice attempt. Answers are real exam answers.

---

## Q1: Duplicate test suggestions — missing existing test context
**Correct:** B — Include existing test file in context so Claude knows what's already covered.
**Why:** Root cause: Claude can only avoid suggesting already-covered scenarios if it knows what tests exist. Context-based solution addresses the actual gap.
**Wrongs:** Reduce count (still duplicates within smaller set), focus on edge cases only (still duplicates edge cases), keyword post-filter (heuristic, misses semantic duplicates).

---

## Q2: Batch vs synchronous — matching API to workflow type
**Correct:** C — Synchronous for blocking PR style checks; Batch for weekly security audits and nightly test generation.
**Why:** Blocking = dev waiting → synchronous. Scheduled/deferred = can tolerate 24hr window → batch (50% savings).
**Wrongs:** Batch for blocking (devs wait 24hrs), sync for everything (misses 50% savings), batch for everything (blocks devs).

---

## Q3: False positive trust erosion — per-category quality variation
**Correct:** C — Temporarily disable high-FP categories (style 52%, naming, docs 48%) and run only high-precision categories (security 8%, performance 18%) while improving prompts.
**Why:** High-FP categories undermine trust in low-FP categories (cascading dismissal). Remove noise immediately; improve prompts offline; re-enable when accurate.
**Wrongs:** Uniform strictness reduction (degrades accurate categories), confidence scores (devs already dismiss all), add few-shot gradually (trust continues eroding during improvement period).

---

## Q4: Self-review bias — confirmation bias in generation
**Correct:** B — Second independent Claude Code instance reviews without seeing generator's reasoning.
**Why:** Eliminates confirmation bias. Mirrors human peer review — different reviewer catches what the original author rationalized away.
**Wrongs:** More context (same reasoning bias persists), self-critique instructions (same reasoning context), extended thinking (same model, same bias).

---

## Q5: Investigation time bottleneck — inline reasoning for triage
**Correct:** A — Include reasoning and confidence assessment inline with each finding.
**Why:** Devs can evaluate without clicking into each finding. Respects constraint against filtering (all findings visible) while making triage faster.
**Wrongs:** Filter high-confidence only (stakeholder rejected filtering), post-process suppress patterns (same), tiered review (changes process, doesn't speed triage).

---

## Q6: Inconsistent output format — few-shot for reliability
**Correct:** C — Add 3-4 few-shot examples showing exact format: issue, location, specific fix.
**Why:** Few-shot examples are most reliable for format consistency when instructions alone produce variable results. Concrete pattern > abstract instructions.
**Wrongs:** More refined instructions (same problem — abstract), more context (doesn't fix format inconsistency), two-pass approach (adds complexity, doesn't guarantee format).

---

## Q7: Vague comment review instructions — explicit criteria
**Correct:** C — Specify explicit criteria: flag only when claimed behavior contradicts actual code behavior.
**Why:** Replaces vague instruction ("check comments are accurate") with precise definition. Eliminates both false positives (TODO markers) and false negatives (stale behavior descriptions).
**Wrongs:** Pre-filter patterns (addresses noise, not misses), git blame data (complex, not about contradiction), few-shot (probabilistic when deterministic criteria available).

---

## Q8: Duplicate findings after fix commits — prior review context
**Correct:** A — Include prior review findings in context; Claude only reports new or still-unaddressed issues.
**Why:** Gives Claude ability to distinguish addressed issues from new ones. Uses reasoning, not post-processing heuristics.
**Wrongs:** Scope restriction to latest commits (misses cross-commit context), skip intermediate commits (no feedback between pushes), post-process filter (heuristic matching, fragile).

---

## Q9: Batch API constraint — iterative tool-calling incompatible
**Correct:** B — Async model prevents executing tools mid-request and returning results for continued analysis.
**Why:** Batch = fire-and-forget. No mechanism to intercept tool call, execute tool, return results within a single logical interaction. Fundamentally breaks iterative tool-calling.
**Wrongs:** No tool definitions (not a real constraint), latency too slow (true but secondary to technical incompatibility), no correlation IDs (not the primary constraint).

---

## Q10: Batch vs sync — blocking vs overnight workflows
**Correct:** B — Batch for overnight technical debt reports only; sync for blocking pre-merge checks.
**Why:** Same decision framework as Q2. Blocking = sync. Overnight/deferred = batch. 24hr latency + no guaranteed SLA vs immediate required.
**Wrongs:** Sync for both (misses savings), batch for both (blocks devs), batch with timeout fallback (complex, unnecessary).

---

## Q11: Batch for deep analysis vs pre-merge hook
**Correct:** C — Deep analysis only (already overnight, tolerates latency, uses polling model).
**Why:** Deep analysis already matches batch characteristics: overnight, polling, latency-tolerant. Pre-merge hook blocks devs = must be sync.
**Wrongs:** Both (blocks merge), pre-merge only (loses savings on deep analysis), neither (misses savings entirely).

---

## Q12: Structured output from CLI — JSON schema enforcement
**Correct:** A — Use `--output-format json` and `--json-schema` to enforce structured findings.
**Why:** Native CLI capability designed for structured output enforcement. Guarantees well-formed JSON with required fields for GitHub API integration.
**Wrongs:** Prompt template instructions (probabilistic, parse failures), summarization step (adds latency + potential errors), CLAUDE.md examples (not enforcement, Claude may still deviate).

---

## Q13: CI pipeline hangs — non-interactive mode
**Correct:** B — Add `-p` flag: `claude -p "Analyze this pull request for security issues"`.
**Why:** `-p` / `--print` is the documented non-interactive mode. Processes prompt, outputs to stdout, exits without waiting for input.
**Wrongs:** `CLAUDE_HEADLESS=true` (not a real env var), `/dev/null` redirect (doesn't prevent interactive prompts), `--batch` flag (doesn't exist for Claude Code CLI).

---

## Q14: Multi-file review inconsistency — multi-pass architecture
**Correct:** B — Per-file analysis for local issues, then separate integration pass for cross-file data flow.
**Why:** Single-pass on 14 files causes attention dilution. Multi-pass ensures consistent depth per file (local) + catches cross-file issues (integration).
**Wrongs:** Smaller PRs (doesn't fix review approach, just limits scope), larger model (more context, same attention dilution), voting across 3 runs (doesn't guarantee quality).

---

## Q15: Inconsistent severity ratings — concrete examples per level
**Correct:** B — Explicit severity criteria with concrete code examples for each severity level.
**Why:** Concrete examples remove ambiguity about what each level means. Proven technique for classification consistency.
**Wrongs:** CLAUDE.md severity mapping (still abstract), reasoning + manual calibration (adds human step, doesn't fix root cause), relative-to-PR rating (creates inconsistency across PRs).

---

## Question Type Distribution

| Type | Count | Questions |
|------|-------|-----------|
| Batch vs synchronous API decisions | 4 (27%) | Q2, Q9, Q10, Q11 |
| Prompt engineering (consistency, criteria) | 3 | Q6, Q7, Q15 |
| Review architecture (multi-pass, self-review) | 2 | Q4, Q14 |
| Structured output & CLI flags | 2 | Q12, Q13 |
| Context inclusion for accuracy | 2 | Q1, Q8 |
| False positives & trust | 2 | Q3, Q5 |

## Dominant Theme: Batch vs Synchronous API Decisions

**4 of 15 questions (27%) test the batch/sync decision framework.** The pattern is consistent:

| Signal | Choose |
|--------|--------|
| Blocking (dev waiting, pre-merge) | Synchronous API |
| Deferred (overnight, weekly, scheduled) | Message Batches API (50% savings) |
| Iterative tool-calling (mid-request tool use) | Synchronous API (batch can't do tool loops) |
| Already uses polling model | Batch API |

## New Patterns NOT In Previous Debrief

1. **Batch API technical incompatibility** (Q9) — Not just "batch is too slow" but batch *fundamentally cannot* support iterative tool-calling. Fire-and-forget model means no mid-request tool interception. This is a structural constraint, not a quality-of-service tradeoff.

2. **False positive trust cascading** (Q3) — High-FP categories (52%, 48%) erode trust in low-FP categories (8%). Fix is NOT uniform adjustment — it's temporarily disabling noisy categories while accurate ones continue. Per-category quality, not aggregate.

3. **Inline reasoning for triage without filtering** (Q5) — When stakeholders reject filtering, the bottleneck isn't finding count but investigation time. Inline reasoning/confidence lets devs triage without clicks. Keep everything visible, speed evaluation.

4. **Prior review findings as context** (Q8) — When re-reviewing after fix commits, include prior findings so Claude can distinguish addressed from new/still-present issues. Prevents redundant feedback.

5. **Explicit criteria > vague instructions** (Q7) — "Check comments are accurate" produces noise + misses. "Flag only when claimed behavior contradicts actual code behavior" is precise, handles both FPs and FNs.

6. **Concrete examples for classification consistency** (Q15) — Not just severity definitions, but concrete code examples per severity level. Makes classification benchmarks unambiguous.

## CLI Flags Tested

| Flag | Purpose | Questions |
|------|---------|-----------|
| `-p` / `--print` | Non-interactive mode for CI/CD | Q13 |
| `--output-format json` | Structured output enforcement | Q12 |
| `--json-schema` | Schema-validated structured output | Q12 |

## Cross-Scenario Pattern Distribution

| Pattern | S1 (Code Gen) | S2 (Multi-Agent) | S3 (CI/CD) |
|---------|:---:|:---:|:---:|
| Context isolation (fork, explore) | 47% | 0 | 0 |
| Error propagation & taxonomy | 0 | 33% | 0 |
| Batch vs synchronous decisions | 0 | 0 | **27%** |
| Prompt engineering (few-shot, criteria) | 7% | 0 | **20%** |
| Config locations/frontmatter | 47% | 0 | 0 |
| Review architecture (multi-pass, self-review) | 0 | 0 | **13%** |
| Structured output & CLI flags | 0 | 0 | **13%** |
| Tool design & scoping | 13% | 20% | 0 |
| Coordinator/subagent architecture | 0 | 27% | 0 |

**Three scenarios, three dominant themes:**
- S1: Configuration & context management (47%)
- S2: Error handling & architecture (33%)
- S3: API decisions & prompt engineering (27% batch + 20% prompt)
