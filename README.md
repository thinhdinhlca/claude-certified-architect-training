# Claude Certified Architect -- Foundations: 12-Week Training Program

**Goal:** Pass the exam (720/1000 minimum) in 12 weeks at 1 hour/day
**Exam format:** Multiple choice (1 correct, 3 distractors), scenario-based, 4 of 6 scenarios randomly selected

## Domain Weightings (study time allocation)

| Domain | Weight | Hours (approx) |
|--------|--------|-----------------|
| D1: Agentic Architecture & Orchestration | 27% | ~23h |
| D2: Tool Design & MCP Integration | 18% | ~15h |
| D3: Claude Code Configuration & Workflows | 20% | ~17h |
| D4: Prompt Engineering & Structured Output | 20% | ~17h |
| D5: Context Management & Reliability | 15% | ~13h |
| Practice exams & review | -- | ~5h |

## 6 Exam Scenarios You Must Master

1. **Customer Support Resolution Agent** -- Agent SDK, MCP tools, escalation
2. **Code Generation with Claude Code** -- CLAUDE.md, plan mode, slash commands
3. **Multi-Agent Research System** -- coordinator-subagent, context passing, error propagation
4. **Developer Productivity with Claude** -- built-in tools, MCP servers, codebase exploration
5. **Claude Code for CI/CD** -- `-p` flag, structured output, batch API, multi-pass review
6. **Structured Data Extraction** -- JSON schemas, tool_use, validation-retry, few-shot

## Weekly Schedule

### Phase 1: Foundations (Weeks 1-4)

#### Week 1: Agentic Loops & Core API (D1.1)
- **Day 1:** Read exam guide domains 1-5. Understand the 6 scenarios.
- **Day 2:** Study agentic loop lifecycle: `stop_reason` ("tool_use" vs "end_turn"), tool result appending
- **Day 3:** Build a minimal agentic loop with the Agent SDK. Implement the control flow.
- **Day 4:** Study anti-patterns: parsing NL for loop termination, arbitrary iteration caps, checking assistant text
- **Day 5:** Practice Test 1 (Agentic Loops -- 10 questions)
- **Day 6:** Review wrong answers. Re-read task statement 1.1.
- **Day 7:** Rest / light review

#### Week 2: Multi-Agent Orchestration (D1.2, D1.3)
- **Day 1:** Study hub-and-spoke architecture, coordinator role, subagent context isolation
- **Day 2:** Study Task tool for subagent spawning, `allowedTools` must include "Task"
- **Day 3:** Build a coordinator + 2 subagents. Practice explicit context passing.
- **Day 4:** Study parallel subagent execution (multiple Task calls in single response), fork_session
- **Day 5:** Study task decomposition pitfalls (overly narrow decomposition = coverage gaps)
- **Day 6:** Practice Test 2 (Multi-Agent Systems -- 10 questions)
- **Day 7:** Rest / review

#### Week 3: Hooks, Workflows & Session Management (D1.4-D1.7)
- **Day 1:** Study PostToolUse hooks for data normalization, tool call interception for compliance
- **Day 2:** Study programmatic enforcement vs prompt-based guidance (deterministic vs probabilistic)
- **Day 3:** Build a hook that blocks refunds above $500 and redirects to escalation
- **Day 4:** Study session management: `--resume`, `fork_session`, named sessions, stale context
- **Day 5:** Study task decomposition: prompt chaining vs dynamic adaptive decomposition
- **Day 6:** Practice Test 3 (Hooks, Workflows & Sessions -- 10 questions)
- **Day 7:** Rest / review

#### Week 4: Tool Design & MCP (D2.1-D2.5)
- **Day 1:** Study tool description best practices: input formats, examples, edge cases, boundaries
- **Day 2:** Study structured error responses: `isError`, `errorCategory`, `isRetryable`, error types
- **Day 3:** Study tool distribution: 4-5 tools per agent max, scoped tool access, `tool_choice` options
- **Day 4:** Study MCP server config: `.mcp.json` (project) vs `~/.claude.json` (user), env var expansion
- **Day 5:** Study built-in tools: Read, Write, Edit, Bash, Grep, Glob -- when to use each
- **Day 6:** Practice Test 4 (Tool Design & MCP -- 10 questions)
- **Day 7:** Rest / review

### Phase 2: Applied Knowledge (Weeks 5-8)

#### Week 5: Claude Code Configuration (D3.1-D3.3)
- **Day 1:** Study CLAUDE.md hierarchy: user (~/.claude/CLAUDE.md), project (.claude/CLAUDE.md), directory
- **Day 2:** Study @import syntax, .claude/rules/ directory for topic-specific rules
- **Day 3:** Study custom slash commands (.claude/commands/) vs skills (.claude/skills/)
- **Day 4:** Study SKILL.md frontmatter: `context: fork`, `allowed-tools`, `argument-hint`
- **Day 5:** Study path-specific rules: YAML frontmatter with `paths` glob patterns
- **Day 6:** Practice Test 5 (Claude Code Config -- 10 questions)
- **Day 7:** Rest / review

#### Week 6: Plan Mode, Iteration & CI/CD (D3.4-D3.6)
- **Day 1:** Study plan mode vs direct execution decision criteria
- **Day 2:** Study iterative refinement: concrete examples, TDD iteration, interview pattern
- **Day 3:** Study CI/CD: `-p` flag, `--output-format json`, `--json-schema`
- **Day 4:** Study session context isolation in CI (generator vs reviewer), prior review findings
- **Day 5:** Study batch processing: Message Batches API, 50% savings, 24h window, `custom_id`
- **Day 6:** Practice Test 6 (Plan Mode & CI/CD -- 10 questions)
- **Day 7:** Rest / review

#### Week 7: Prompt Engineering & Structured Output (D4.1-D4.3)
- **Day 1:** Study explicit criteria over vague instructions, false positive impact on developer trust
- **Day 2:** Study few-shot prompting: 2-4 examples for ambiguous cases, format consistency
- **Day 3:** Study tool_use with JSON schemas: guaranteed schema compliance, semantic errors still possible
- **Day 4:** Study tool_choice: "auto" vs "any" vs forced `{"type": "tool", "name": "..."}`
- **Day 5:** Study schema design: required vs optional, enums with "other" + detail, nullable fields
- **Day 6:** Practice Test 7 (Prompt Engineering -- 10 questions)
- **Day 7:** Rest / review

#### Week 8: Validation, Batch, Multi-Pass (D4.4-D4.6)
- **Day 1:** Study validation-retry loops: append specific errors to prompt, when retries are ineffective
- **Day 2:** Study `detected_pattern` fields for tracking dismissal patterns
- **Day 3:** Study batch processing strategy: synchronous for blocking, batch for latency-tolerant
- **Day 4:** Study self-review limitations: same session retains reasoning context
- **Day 5:** Study multi-pass review: per-file local analysis + cross-file integration pass
- **Day 6:** Practice Test 8 (Validation & Multi-Pass -- 10 questions)
- **Day 7:** Rest / review

### Phase 3: Context & Reliability + Exam Prep (Weeks 9-12)

#### Week 9: Context Management (D5.1-D5.3)
- **Day 1:** Study progressive summarization risks, "lost in the middle" effect
- **Day 2:** Study "case facts" blocks, trimming verbose tool outputs, position-aware ordering
- **Day 3:** Study escalation patterns: customer demands, policy gaps, sentiment != complexity
- **Day 4:** Study error propagation: structured context vs generic errors, access failures vs empty results
- **Day 5:** Study local recovery before coordinator escalation, partial results + what was attempted
- **Day 6:** Practice Test 9 (Context & Reliability -- 10 questions)
- **Day 7:** Rest / review

#### Week 10: Advanced Context & Provenance (D5.4-D5.6)
- **Day 1:** Study context degradation in extended sessions, scratchpad files
- **Day 2:** Study /compact, subagent delegation for verbose exploration, crash recovery manifests
- **Day 3:** Study human review: stratified sampling, field-level confidence, accuracy by doc type
- **Day 4:** Study information provenance: claim-source mappings, temporal data, conflict annotation
- **Day 5:** Study synthesis output: distinguish well-established vs contested, preserve source characterizations
- **Day 6:** Practice Test 10 (Advanced Context -- 10 questions)
- **Day 7:** Rest / review

#### Week 11: Integration & Hands-On Exercises
- **Day 1:** Complete Exercise 1 from exam guide (Multi-Tool Agent with Escalation Logic)
- **Day 2:** Complete Exercise 2 (Claude Code Team Workflow Configuration)
- **Day 3:** Complete Exercise 3 (Structured Data Extraction Pipeline)
- **Day 4:** Complete Exercise 4 (Multi-Agent Research Pipeline)
- **Day 5:** Full Practice Exam 1 (50 questions, all 6 scenarios)
- **Day 6:** Review all wrong answers, identify weak domains
- **Day 7:** Rest / review weak areas

#### Week 12: Final Exam Prep
- **Day 1:** Targeted review of weakest domain
- **Day 2:** Targeted review of second weakest domain
- **Day 3:** Full Practice Exam 2 (50 questions, all 6 scenarios)
- **Day 4:** Review wrong answers, fill gaps
- **Day 5:** Full Practice Exam 3 (50 questions, timed)
- **Day 6:** Light review of key concepts, anti-patterns, and gotchas
- **Day 7:** Exam day (or rest before exam)

## Key Anti-Patterns to Memorize

These come up repeatedly in exam questions as wrong answers:

1. **Parsing natural language** for loop termination instead of checking `stop_reason`
2. **Arbitrary iteration caps** as primary stopping mechanism
3. **Prompt-based enforcement** for critical business rules (use programmatic hooks)
4. **Self-reported confidence scores** for escalation decisions (unreliable)
5. **Sentiment-based escalation** (sentiment != complexity)
6. **Generic error messages** ("Operation failed") hiding context
7. **Silently suppressing errors** (returning empty results as success)
8. **Too many tools** per agent (18 vs 4-5 degrades selection)
9. **Same-session self-review** (retains reasoning context bias)
10. **Aggregate accuracy metrics** masking per-document-type failures

## Key Decision Frameworks

| Decision | Choose A | Choose B |
|----------|----------|----------|
| Enforcement method | **Programmatic hooks** when errors have financial/safety consequences | **Prompt instructions** when best-effort is acceptable |
| Plan mode vs direct | **Plan mode** for multi-file, architectural, multiple valid approaches | **Direct execution** for single-file, clear scope, obvious fix |
| Tool_choice | **"any"** to guarantee a tool call | **forced** to ensure a specific tool runs first |
| API type | **Synchronous** for blocking workflows (pre-merge checks) | **Batch** for latency-tolerant (overnight reports) |
| Error handling | **Structured error context** with category, retry flag, partial results | Never generic messages or silent suppression |
| Escalation | **Immediate** for explicit customer request | **Resolve first** when issue is within capability |
| Review architecture | **Multi-pass** (per-file + integration) for large PRs | **Single-pass** only for small, focused changes |
| Context passing | **Explicit** in subagent prompts | Never rely on automatic inheritance |
