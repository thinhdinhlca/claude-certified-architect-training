# Exam Debrief — First Practice Test Attempt

> Based on grill-me session after completing Practice Test 1 (Agentic Loops).
> Date: 2026-05-17

---

## Exam Format

| Detail | Value |
|--------|-------|
| Total questions | 60 |
| Time limit | 90 minutes |
| Time per question | ~1.5 min |
| Scenarios | 4 of 6 canonical scenarios (randomly selected) |
| Questions per scenario | ~15 |
| Question structure | Self-contained micro-scenarios (not a continuing narrative) |
| Cross-domain | Single scenario can test multiple domains |
| Scenario presentation | Context embedded into each question (not a big block upfront) |

## Pacing

- Finished with **30-40 min buffer**
- Started by skimming → hurt early scores
- Got better results when reading carefully from the start
- **Recommendation**: Slow down from question 1. Use the buffer on the first pass, not as a safety net.

## Difficulty Gap vs Practice Tests

**Gap: 5-6 out of 10.** Real exam questions are:

1. **More verbose** — require active re-reading and highlighting
2. **Denser with constraints** — the key detail that eliminates the almost-right answer is buried in the scenario
3. **Cross-domain within a single question** — not siloed by domain
4. **Hands-on focused** — not theoretical. Requires knowing exact field names, config paths, flag names
5. **Distractors are well-crafted** — not obviously wrong, similar length, no gimmicks ("all of the above", extreme language)

## What to Highlight When Reading

1. **Technical constraints** — "latency-tolerant", "blocking", "financial impact"
2. **Already-accepted/rejected approaches** in the scenario — don't re-litigate them
3. **Anti-pattern keywords** in wrong answers — "parse the response", "self-reported confidence", "sentiment-based"

## Anti-Patterns That Showed Up

Confirmed from the README list:
- Silently suppressing errors
- Sentiment-based escalation
- Parsing natural language for loop termination
- Arbitrary iteration caps as primary stopping mechanism
- Prompt-based enforcement for critical business rules

Additional anti-patterns encountered:
- Few-shot examples used as a band-aid for deeper design problems
- Giving agents too many tools (4-5 max)
- Same-session self-review

## Failure Modes Tested (All Four Categories)

1. **Tool failures** — tool returns error, what does agent do?
2. **Context limits** — session too long, what gets lost?
3. **API errors** — rate limits, timeouts, partial responses
4. **Model behavior** — hallucinated tool calls, wrong tool selection, infinite loops

## Domain-Specific Findings

### Agentic Loops (D1)
- `stop_reason` values: `"tool_use"`, `"end_turn"`, `"max_tokens"` — exact knowledge required
- Content array can contain both text and tool_use blocks in same response
- Tool results must be appended to conversation history

### Multi-Agent Orchestration (D1)
- Subagents are **isolated by default** — don't share full context
- Coordinator must **explicitly pass** context in subagent prompts
- **fork_session**: use when preventing context pollution (parallel tasks shouldn't see each other's intermediate steps)
- Parallel vs sequential execution tested
- Error propagation from subagents tested
- Subagent prompt details rarely tested directly

### Hooks & Workflows (D1)
- PostToolUse hooks tested — what they can do, when they're the right answer
- Hook type identification (PostToolUse vs other options)
- Deterministic enforcement vs prompt-based guidance

### Tool Design & MCP (D2)
- Config file locations: `.mcp.json` (project) vs `~/.claude.json` (user)
- Tool scoping: which agents get which tools
- Access restriction: preventing dangerous actions (e.g., deletion)
- Least-privilege design
- MCP server behavior and tool discovery

### Claude Code Configuration (D3)
- CLAUDE.md hierarchy: directory > project > user (most specific wins)
- Conflict resolution between levels tested heavily
- `.claude/rules/` for topic-specific organization
- `@import` syntax for selective inclusion
- Custom slash commands (`.claude/commands/`) — invoked with `/command-name`
- Skills (`.claude/skills/`) — `SKILL.md` with frontmatter (`context: fork`, `allowed-tools`, `argument-hint`)
- Commands vs skills: commands for quick shortcuts, skills for complex workflows with restrictions
- Personal variants in `~/.claude/` with different names

### Plan Mode & CI/CD (D3)
- Plan mode vs direct execution decision framework tested
- Batch API: when to use (latency-tolerant, overnight, 50% savings) vs when not to (blocking CI)
- `-p` flag tested
- Mechanics of batching less tested than decision framework

### Prompt Engineering & Structured Output (D4)
- Few-shot examples: correct for format ambiguity, wrong as band-aid for deeper problems
- Schema design decisions (required vs optional, enums with "other" + detail)
- Validation-retry loops: when to stop retrying

### Context Management & Reliability (D5)
- "Lost in the middle" effect tested
- Progressive summarization: when NOT to summarize, how to summarize safely
- Position-aware ordering
- Escalation patterns tested heavily

### Escalation Patterns
- Tiebreaker details: policy gap, inefficiency, agent capability/authority
- Customer phrase analysis — understanding why it caused the error
- Immediate escalation for explicit requests, resolve first when within capability
- Never use sentiment or self-reported confidence as triggers

## Question Construction Patterns

- All questions scenario-anchored
- Decision-focused: "best approach", "what should you do", "what is the root cause"
- Wrong answers are negated by a specific constraint in the question text
- No obvious test-taking heuristics work (length, extreme language, "all of the above")
- Detailed explanations provided for each answer (why correct, why each distractor is wrong)

## Study Recommendations

### Flashcard Priority (All Were Tested)
1. API fields (`stop_reason` values, `tool_choice` options, `isError`/`isRetryable`)
2. Config files (`.mcp.json` vs `~/.claude.json`, CLAUDE.md hierarchy, `.claude/commands/` vs `.claude/skills/`)
3. Flag names (`-p`, `--output-format json`, `--json-schema`, `fork_session`)
4. Error categories (structured error response taxonomy)
5. SKILL.md frontmatter fields (`context: fork`, `allowed-tools`, `argument-hint`)

### Practice Test Improvements
- Questions must relate to one of the 6 canonical scenarios
- More verbose, with embedded constraints
- Answer choices should have similar length
- Answers must be carefully structured to test thinking, not obviously wrong
- Include detailed explanations for every answer (why correct, why each distractor is wrong)
- Focus on hands-on implementation details, not just theory
- Include failure mode scenarios at every layer (tool, context, API, model behavior)

### Tactical Advice for Colleagues
1. **Read carefully from the start** — skimming early hurts scores
2. **Highlight constraints** — the key detail that eliminates the almost-right answer
3. **Memorize anti-patterns** — at least a third of questions test spotting wrong approaches
4. **Know exact syntax** — field names, config paths, flag names
5. **Understand failure modes** — tested repeatedly at every layer
6. **Practice decision frameworks** — exam asks "which approach?" not "what is X?"
7. **Use the buffer time** — 30-40 min buffer exists for a reason

---

---

## Update: Scenario 1 Analysis (Code Generation with Claude Code)

After analyzing 15 real exam questions from Scenario 1:

### New Patterns Discovered

1. **`.claude/rules/` with YAML frontmatter glob patterns** — Path-specific conditional rule application using glob patterns (`**/*.test.tsx`, `src/api/**/*.ts`). Solves "different conventions for different file types scattered throughout codebase." Files activate automatically and deterministically based on file path.

2. **Explore subagent** — Specific subagent type for verbose discovery/scanning tasks. Isolates verbose output in separate context, returns concise summary. Used when context window is at risk from verbosity (Q15: scanning 120-file codebase).

3. **Combined skill configuration** — Questions that test multiple frontmatter features simultaneously (e.g., `argument-hint` + `context: fork` + `allowed-tools`) to solve a multi-symptom problem. Tests whether you can match the right feature to each symptom.

4. **Skills for on-demand exemplar loading** — Exemplar/pattern code only needed for specific tasks (creating new endpoints), not for all tasks. Skills invoked on-demand prevent unnecessary context bloat.

5. **Concrete examples (few-shot) as answer to prose ambiguity** — When requirements are misinterpreted by Claude, providing concrete input-output examples beats more precise prose, JSON schemas, or asking Claude to explain itself. Targets root cause: ambiguity in prose description.

6. **MCP env var expansion `${GITHUB_TOKEN}`** — Pattern for team-wide MCP config without credentials. Project-scoped `.mcp.json` + `${ENV_VAR}` = single source of truth + per-dev credential injection.

7. **Personal skill naming collision** — Project skills take precedence over personal skills with the same name. Must use a different name in `~/.claude/skills/`.

### Question Type Distribution (Scenario 1)

| Type | Count |
|------|-------|
| Plan mode vs direct execution | 2 |
| Skills configuration (frontmatter, isolation) | 5 |
| Skills vs CLAUDE.md (what goes where) | 2 |
| CLAUDE.md organization (rules/, hierarchy) | 3 |
| MCP configuration | 1 |
| Custom commands location | 1 |
| Concrete examples / few-shot | 1 |
| Subagent delegation (Explore) | 1 |
| Personal skill customization | 1 |

### Dominant Theme: Context Management via Configuration

A clear pattern across 15 questions: **the right answer often involves isolating context to prevent pollution or only loading context when needed.**

- `context: fork` appeared as the correct answer in 3 questions (Q5, Q11, Q13)
- Skills on-demand loading in 2 questions (Q7, Q8)
- Explore subagent for isolation in 1 question (Q15)
- `.claude/rules/` glob patterns for conditional loading in 1 question (Q10)

**7 of 15 questions (47%) revolve around "load the right context at the right time."**

### Confirmed Debrief Patterns

- ✅ Exact syntax knowledge required (`context: fork`, `allowed-tools`, `argument-hint`, `${GITHUB_TOKEN}`)
- ✅ Config file locations heavily tested (`.claude/commands/`, `.claude/rules/`, `.mcp.json`, `~/.claude/skills/`)
- ✅ Answers of similar length, no gimmicks
- ✅ Scenario-anchored, every question under "Code Generation with Claude Code"
- ✅ Detailed explanations for each answer
- ✅ Distractors are plausible but wrong for a specific constraint-based reason

---

---

## Update: Scenario 2 Analysis (Multi-Agent Research System)

After analyzing 15 real exam questions from Scenario 2:

### Dominant Theme: Error Propagation & Structured Context

**5 of 15 questions (33%) test error handling decisions.** The nuance: not just "should errors be propagated" but **how errors should be structured, categorized, and annotated**.

### New Patterns Discovered

1. **Error taxonomy distinction** — Access failure (timeout = retryable) is semantically different from valid empty result ("0 results" = informative outcome). Distinguish categories; don't conflate into a single metric.

2. **Coverage annotations / transparency** — Output must indicate which findings are well-supported and which areas have gaps due to unavailable sources. Graceful degradation with transparency, not silent omission.

3. **Least privilege via tool interface design** — Replace general-purpose tools (`fetch_url`) with domain-specific ones (`load_document` that validates URL points to document format). Make undesired behavior impossible, not just discouraged by prompts.

4. **Scoped capabilities for common cases** — Give agent a focused tool (`verify_fact`) for 85% of cases; complex 15% still route through coordinator. Balance least privilege with practical optimization.

5. **Tool naming overlap as misrouting root cause** — `analyze_content` (web agent) vs `analyze_document` (doc agent) causes coordinator confusion. Fix: unique, unambiguous names (`extract_web_results`).

6. **Structured data over verbose content** — Subagents should return structured data (key facts, citations, relevance scores) instead of raw page content and reasoning chains. Reduces token volume at the source.

7. **Task partitioning before delegation** — Coordinator explicitly partitions research space before subagents run. Prevents overlap without losing parallelism.

8. **Local recovery before escalation** — Subagent handles transient failures locally (with context of attempts), only escalates persistent/unresolvable errors.

### Question Type Distribution

| Type | Count |
|------|-------|
| Error propagation & handling | 5 (33%) |
| Coordinator architecture | 2 |
| Task decomposition & partitioning | 2 |
| Tool design & scoping (least privilege) | 3 |
| Context & token management | 2 |
| Conflict handling | 1 |

### Cross-Scenario Pattern Comparison

| Pattern | Scenario 1 (Code Gen) | Scenario 2 (Multi-Agent) |
|---------|----------------------|--------------------------|
| Context isolation (fork, explore) | 7 questions (47%) | 0 |
| Error propagation & taxonomy | 0 | 5 questions (33%) |
| Tool design & scoping | 2 | 3 |
| Coordinator/subagent architecture | 0 | 4 |
| Config locations/frontmatter | 7 | 0 |
| Plan mode vs direct | 2 | 0 |
| Task decomposition | 0 | 2 |
| Concrete examples/few-shot | 1 | 0 |

**Key insight:** Each scenario has a distinct gravitational pull. Scenario 1 = configuration-driven context management. Scenario 2 = error propagation & architecture patterns.

---

**Three scenarios, three dominant themes:**
- S1: Configuration & context management (47%)
- S2: Error handling & architecture (33%)
- S3: API decisions & prompt engineering (27% batch + 20% prompt)

---

## Update: Scenario 3 Analysis (Claude Code for CI/CD)

After analyzing 15 real exam questions from Scenario 3:

### Dominant Theme: Batch vs Synchronous API Decisions

**4 of 15 questions (27%) test the batch/sync framework.** Decision rule:
- Blocking (dev waiting, pre-merge) → **Synchronous**
- Deferred (overnight, weekly, scheduled) → **Batch** (50% savings)
- Iterative tool-calling workflows → **Synchronous** (batch can't do tool loops)

### New Patterns

1. **Batch API technical incompatibility** — Not just "too slow" but fundamentally cannot support iterative tool-calling. Fire-and-forget = no mid-request tool interception.

2. **False positive trust cascading** — High-FP categories (52%) erode trust in low-FP categories (8%). Fix: temporarily disable noisy categories, not uniform adjustment.

3. **Inline reasoning for triage without filtering** — When filtering is rejected, inline reasoning/confidence speeds evaluation while keeping all findings visible.

4. **Prior review findings as context** — Include prior findings so Claude distinguishes addressed from new/remaining issues on re-review.

5. **Explicit criteria > vague instructions** — "Check comments are accurate" → "Flag only when claimed behavior contradicts actual code behavior."

6. **Concrete examples for classification consistency** — Not just severity definitions, but concrete code examples per level.

### CLI Flags Tested
- `-p` / `--print` — non-interactive CI/CD mode
- `--output-format json` + `--json-schema` — structured output enforcement

### Question Distribution
- Batch vs sync: 4 Qs (27%)
- Prompt engineering: 3 Qs (20%)
- Review architecture: 2 Qs (13%)
- Structured output & CLI: 2 Qs (13%)
- Context for accuracy: 2 Qs
- FP/trust: 2 Qs

### Three-Scenario Pattern Map

| Pattern | S1 | S2 | S3 |
|---------|:--:|:--:|:--:|
| Context isolation | **47%** | 0 | 0 |
| Error propagation | 0 | **33%** | 0 |
| Batch vs sync | 0 | 0 | **27%** |
| Prompt engineering | 7% | 0 | **20%** |
| Review architecture | 0 | 0 | **13%** |
| Config/frontmatter | **47%** | 0 | 0 |
| Tool scoping | 13% | **20%** | 0 |
| Coordinator arch | 0 | **27%** | 0 |

---

---

## Update: Scenario 4 Analysis (Customer Support Resolution Agent)

After analyzing 15 real exam questions from Scenario 4:

### Dominant Theme: Tool Selection Reliability (27%)

Multi-layered fix spectrum: tool descriptions → programmatic enforcement → prompt guidance → keyword steering diagnosis.

### ⚠️ Critical Traps: Few-Shot Decision Boundaries

User got Q5 and Q9 wrong, revealing a critical distinction:

| Signal | Correct Answer | Why |
|--------|---------------|-----|
| "Specific context gaps vary by case" (Q5) | **Self-critique** (evaluator-optimizer) | Few-shot can't cover variable patterns |
| "Agent already handles single concerns at 94%" (Q9) | **Few-shot examples** | Strong baseline → don't over-engineer |

**Decision rule:** Few-shot wins for consistent patterns. Self-critique/architectural approaches win for variable, unpredictable gaps. Don't default to few-shot reflexively.

### New Patterns

1. Persistent "case facts" block for preserving precise details through summarization
2. Keyword-sensitive prompt instructions as root cause of tool selection bias
3. Parallel decomposition with shared context for complex multi-concern requests
4. User disambiguation over probabilistic heuristics (ask for clarifying info)
5. Tool batching via prompt ("batch related requests per turn")

### Four-Scenario Complete Map

| Pattern | S1 (Code) | S2 (Multi-Ag) | S3 (CI/CD) | S4 (Support) |
|---------|:--:|:--:|:--:|:--:|
| Context isolation | **47%** | — | — | — |
| Error propagation | — | **33%** | — | — |
| Batch vs sync API | — | — | **27%** | — |
| Tool selection | — | — | — | **27%** |
| Prompt engineering | 7% | — | **20%** | 13% |
| Config/frontmatter | **47%** | — | — | — |
| Escalation | — | — | — | 13% |
| Tool scoping | 13% | **20%** | — | — |
| Coordinator arch | — | **27%** | — | — |

---

## Next Steps

- [ ] Generate improved practice tests with constraints from this debrief
- [ ] Create flashcards for all syntax/config/API details
- [ ] Build failure mode scenarios for each domain
- [ ] Re-attempt practice tests with careful reading strategy
- [ ] Update this debrief after next test attempt
