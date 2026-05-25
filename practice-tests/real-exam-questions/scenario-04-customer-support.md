# Scenario 4: Customer Support Resolution Agent (15 Questions)

> Pasted from real exam practice attempt. Answers are real exam answers.
> ⚠️ User got Q5 and Q9 wrong — key patterns to study.

---

## Q1: Wrong tool selection — diagnostic first step
**Correct:** C — Review tool descriptions to ensure they clearly distinguish each tool's purpose.
**Why:** Tool descriptions are the primary input for tool selection. When agent consistently picks wrong tool, examine descriptions first.
**Wrongs:** Few-shot for every pattern (exhaustive, doesn't fix root cause), pre-processing classifier (adds complexity before diagnosing), reduce tools (doesn't fix description ambiguity).

---

## Q2: Summarization losing precise transaction details
**Correct:** A — Extract transactional facts (amounts, dates, order numbers) into persistent "case facts" block outside summarized history.
**Why:** Summarization is inherently lossy for precise details. Persistent structured block preserves critical facts regardless of turn count.
**Wrongs:** Increase threshold (delays, doesn't prevent loss), revise summarization prompt (still lossy), external retrieval (adds complexity when persistence is simpler).

---

## Q3: Escalation calibration — 55% resolution, escalates simple, handles complex
**Correct:** B — Add explicit escalation criteria with few-shot examples demonstrating when to escalate vs resolve.
**Why:** Root cause is unclear decision boundaries. Few-shot criteria directly teaches the agent without additional infrastructure.
**Wrongs:** Self-reported confidence (anti-pattern — unreliable), separate classifier (over-engineering), sentiment-based (anti-pattern — sentiment ≠ complexity).

---

## Q4: Similar tool descriptions causing selection errors
**Correct:** A — Expand tool descriptions with input formats, example queries, edge cases, and boundaries vs similar tools.
**Why:** Low-effort, high-leverage fix that improves the primary mechanism LLMs use for tool selection.
**Wrongs:** Few-shot in system prompt (works but doesn't fix root cause — descriptions), pre-parsing router (adds complexity), consolidate tools (loses specificity).

---

## Q5: ⚠️ USER GOT WRONG — Self-critique vs few-shot for variable context gaps
**User's answer:** D — Few-shot examples for 5 common case types.
**Correct:** A — Self-critique step (evaluator-optimizer) evaluating draft against criteria (policy context, timelines, next steps).
**Why few-shot is wrong here:** "Specific context gaps vary by case" means few-shot can't cover the variation. Self-critique catches case-specific gaps regardless of type.
**When few-shot wins:** Consistent, predictable patterns. **When self-critique wins:** Variable gaps across diverse scenarios.
**Study area:** Self-Evaluation Patterns — evaluator-optimizer pattern.

---

## Q6: Data normalization across MCP tools (third-party, unmodifiable)
**Correct:** A — PostToolUse hook to intercept tool results and apply formatting transformations.
**Why:** Centralized, deterministic normalization point. Works for third-party tools you can't modify. Uniform via code, not LLM interpretation.
**Wrongs:** New normalize tool (adds tool call overhead), system prompt docs (relies on LLM interpretation), wrappers (maintenance burden for each third-party tool).

---

## Q7: Appropriate escalation trigger — policy gap
**Correct:** B — Price match: policies are silent on competitor pricing → escalate for policy interpretation.
**Why:** Genuine policy gap where agent cannot fabricate a policy. Must escalate for human judgment.
**Wrongs:** Multi-issue (agent can handle both — not an escalation trigger), contradictory evidence (agent can present facts objectively), cancel shipped (agent can explain policy).

---

## Q8: Agent skips customer verification — programmatic prerequisite
**Correct:** C — Programmatic prerequisite blocking `lookup_order` and `process_refund` until `get_customer` returns verified customer ID.
**Why:** Deterministic guarantee that required sequence is followed. Removes possibility of bypass regardless of LLM behavior.
**Wrongs:** Few-shot (probabilistic), prompt instructions (same), routing classifier (complex, doesn't enforce sequence).

---

## Q9: ⚠️ USER GOT WRONG — Few-shot vs preprocessing for multi-concern
**User's answer:** D — Preprocessing layer decomposing multi-concern into individual requests.
**Correct:** A — Few-shot examples demonstrating correct reasoning and tool sequence for multi-concern.
**Why preprocessing is wrong here:** Agent already handles single concerns at 94% — preprocessing adds unnecessary latency, complexity, cost when simple prompt guidance works. "Agent already demonstrates strong single-concern understanding" → don't over-engineer.
**When preprocessing wins:** Fundamental architecture limitation. **When few-shot wins:** Strong single-concern baseline, just needs multi-concern pattern guidance.
**Study area:** Tool Selection Reliability.

---

## Q10: Complex multi-concern handling — parallel decomposition with shared context
**Correct:** C — Decompose into distinct concerns, investigate each in parallel with shared customer context.
**Why:** Eliminates redundant data fetching (shared context) AND reduces total tool calls (parallelization). Addresses both 12+ calls and redundant data gathering.
**Wrongs:** Verification gates (adds turns), few-shot (doesn't fix sequential investigation), consolidate tools (loses specificity).

---

## Q11: Keyword-sensitive prompt instructions causing tool bias
**Correct:** A — System prompt contains keyword-sensitive instructions ("account") creating unintended steering.
**Why:** Systematic pattern (78% vs 93%) signals routing logic reacting to specific words. Tool descriptions are already fine — problem is in prompt instructions.
**Wrongs:** Fine-tuning (unnecessary, not root cause), base training associations (descriptions override this), negative examples in descriptions (descriptions are fine).

---

## Q12: Multi-match customer lookup — ask user for disambiguation
**Correct:** C — Ask for additional identifier (email, phone, order number) when multiple matches returned.
**Why:** User has definitive knowledge of their identity. One extra turn is cheaper than 15% error rate from wrong customer selection.
**Wrongs:** Confidence scoring (unreliable self-reported confidence anti-pattern), single-return ranking (hides ambiguity), conversational inference from context (probabilistic).

---

## Q13: Agentic loop continuation decision
**Correct:** B — Check `stop_reason`: continue on `"tool_use"`, stop on `"end_turn"`.
**Why:** `stop_reason` is the canonical, API-provided mechanism for loop control. Not NL parsing, not iteration caps, not content type checking.
**Wrongs:** Parse for completion phrases (NL parsing anti-pattern), iteration cap as primary (should be safety fallback), check for text content (content can coexist with tool_use).

---

## Q14: Few-shot for ambiguous tool selection — targeted at edge cases
**Correct:** D — 4-6 examples targeting ambiguous scenarios, each showing reasoning for why one tool was chosen over alternatives.
**Why:** Worked examples with comparative reasoning directly teach the decision-making process for edge cases. Better than declarative rules.
**Wrongs:** Grouped by tool (no comparative reasoning), "use when" guidelines (declarative, not worked), generic clear examples (doesn't target the actual ambiguous scenarios).

---

## Q15: Reducing API round-trips — batch tool requests per turn
**Correct:** B — Prompt Claude to batch related tool requests per turn, return all results together before next call.
**Why:** Leverages Claude's native ability to request multiple tools simultaneously. Minimal architectural change.
**Wrongs:** Speculative execution (calls unnecessary tools), increase max_tokens (more space ≠ batching behavior), composite tools (maintenance burden, explosion of combinations).

---

## Question Type Distribution

| Type | Count | Questions |
|------|-------|-----------|
| Tool selection & description | 4 (27%) | Q1, Q4, Q8, Q14 |
| Escalation decisions | 2 | Q3, Q7 |
| Multi-concern/complex request handling | 2 | Q9, Q10 |
| Context management (case facts) | 2 | Q2, Q15 |
| Data normalization (hooks) | 1 | Q6 |
| Self-evaluation (evaluator-optimizer) | 1 | Q5 |
| Agentic loop control | 1 | Q13 |
| Prompt instruction analysis | 1 | Q11 |
| Ambiguous matching | 1 | Q12 |

## Dominant Theme: Tool Selection Reliability

**4 of 15 questions (27%) test tool selection decisions.** The pattern is multi-layered:

| Layer | Fix | Questions |
|-------|-----|-----------|
| Tool descriptions (root cause) | Expand descriptions with inputs, examples, boundaries | Q1, Q4 |
| Programmatic enforcement | Block downstream tools until prerequisites met | Q8 |
| Prompt-level guidance | Few-shot ambiguous scenarios, keyword steering diagnosis | Q11, Q14 |
| System design | Parallel decomposition, batching, disambiguation | Q10, Q12, Q15 |

## ⚠️ Traps to Study (Questions User Got Wrong)

**Q5 Trap: Few-shot vs Self-Critique**
- Signal for few-shot: Consistent, predictable gaps ("always missing policy detail")
- Signal for self-critique: Variable gaps across cases ("sometimes omitting policy, other times timeline")
- Self-critique catches case-specific gaps. Few-shot only covers patterns in examples.

**Q9 Trap: Few-shot vs Preprocessing**
- Signal for few-shot: High single-concern accuracy (94%) — just needs multi-concern pattern guidance
- Signal for preprocessing: Fundamental architectural limitation, not just a guidance gap
- When baseline is strong, don't add architectural layers. Add pattern examples.

## Cross-Scenario Pattern Distribution (Complete)

| Pattern | S1 (Code Gen) | S2 (Multi-Agent) | S3 (CI/CD) | S4 (Support) |
|---------|:--:|:--:|:--:|:--:|
| Context isolation (fork, explore) | 47% | — | — | — |
| Error propagation & taxonomy | — | 33% | — | — |
| Batch vs sync API decisions | — | — | 27% | — |
| **Tool selection & description** | — | — | — | **27%** |
| Prompt engineering (few-shot, criteria) | 7% | — | 20% | 13% |
| Config locations/frontmatter | 47% | — | — | — |
| Escalation decisions | — | — | — | 13% |
| Review architecture | — | — | 13% | — |
| Structured output & CLI flags | — | — | 13% | — |
| Tool design & scoping | 13% | 20% | — | — |
| Coordinator/subagent architecture | — | 27% | — | — |
| Multi-concern/complex handling | — | — | — | 13% |
| Data normalization (hooks) | — | — | — | 7% |
| Self-evaluation patterns | — | — | — | 7% |

**Four scenarios, four gravitational pulls:**
- S1: Configuration & context management (47%)
- S2: Error handling & multi-agent architecture (33%)
- S3: API decisions & prompt engineering (27% + 20%)
- S4: Tool selection reliability & escalation (27% + 13%)
