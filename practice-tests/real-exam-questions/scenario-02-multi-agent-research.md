# Scenario 2: Multi-Agent Research System (15 Questions)

> Pasted from real exam practice attempt. Answers are real exam answers.

---

## Q1: Error propagation — distinct semantic outcomes (timeout vs "0 results")
**Correct:** Distinguish access failures (timeout → retry) from valid empty results ("0 results" → informative finding).
**Why:** Timeout (access failure) and "0 results" (valid empty) are semantically distinct outcomes requiring different responses. Conflating them loses information.
**Wrongs:** Aggregate metric (loses distinction), treat both as failures (causes unnecessary retries), internal retry only (hides transient vs persistent information from coordinator).

---

## Q2: Structured error context for coordinator recovery
**Correct:** Return structured error context including failure type, attempted query, partial results, and alternative approaches.
**Why:** Gives coordinator maximum information for intelligent recovery decisions — retry with modified query or proceed with partial results.
**Wrongs:** Terminate workflow (loses all progress), return empty as success (hides failure), generic "search unavailable" after retries (loses query context).

---

## Q3: Coverage gap — coordinator decomposition too narrow
**Correct:** Coordinator decomposed "impact of AI on creative industries" into only visual arts subtasks (digital art, graphic design, photography). Subagents all performed correctly — problem is the decomposition.
**Why:** Coordinator logs directly show narrow decomposition. Root cause is not in subagents since they executed assigned tasks correctly.
**Wrongs:** Web search not comprehensive (subagent executed correctly), analysis agent filtering (same), synthesis missing gap detection (symptom not cause).

---

## Q4: Coordinator as central hub — advantage
**Correct:** Centralized visibility into all interactions, consistent error handling, fine-grained control over what each subagent receives.
**Why:** Hub-and-spoke provides observability, error consistency, and information routing control.
**Wrongs:** Batching (not primary benefit), auto-retry (not coordinator-specific), serialization complexity (not main advantage).

---

## Q5: Duplicated work across parallel subagents
**Correct:** Coordinator explicitly partitions research space before delegation, assigning distinct subtopics or source types.
**Why:** Addresses root cause (unclear task boundaries) before work begins, preserving parallel execution benefits.
**Wrongs:** Deduplicate after (wastes tokens), shared state logging (complex coordination overhead), sequential execution (loses parallelism).

---

## Q6: Post-research integration flow
**Correct:** Coordinator passes both sets of findings to synthesis agent for unified integration.
**Why:** Orchestrator-workers pattern: coordinator collects results, routes to next appropriate component (synthesis agent designed for unification).
**Wrongs:** Agent-to-agent merging (bypasses coordinator), raw concatenation (loses synthesis), direct to report generation (bypasses synthesis step).

---

## Q7: Local recovery before escalation
**Correct:** Subagent implements local recovery for transient failures, only escalates unresolvable errors with context of what was attempted + partial results.
**Why:** Handle at lowest capable level. Reduces unnecessary coordinator involvement while preserving full context for escalation.
**Wrongs:** Coordinator pre-validates (moves burden up), dedicated error-handling agent (adds complexity), always return success (hides failures).

---

## Q8: Conflicting statistics from credible sources
**Correct:** Complete analysis with both figures, annotate conflict with source attribution, let coordinator decide reconciliation.
**Why:** Respects separation of concerns: analysis agent completes task without blocking, preserves conflicting data with attribution, defers reconciliation to coordinator with broader context.
**Wrongs:** Don't flag conflict (hides uncertainty), apply heuristics to pick one (loses context/attribution), halt and escalate (blocks progress unnecessarily).

---

## Q9: Tool scope — preventing ad-hoc web searches by wrong agent
**Correct:** Replace general `fetch_url` with scoped `load_document` tool that validates URLs point to document formats.
**Why:** Addresses root cause at interface level — makes undesired behavior impossible (least privilege), not merely discouraged (prompt instructions).
**Wrongs:** Prompt instructions (probabilistic), route through coordinator (adds latency), domain filtering (whack-a-mole on URL patterns).

---

## Q10: Scoped tool for simple fact verification (85% lookups)
**Correct:** Give synthesis agent `verify_fact` tool for simple lookups; complex verifications (15%) still go through coordinator → web search agent.
**Why:** Eliminates round-trips for 85% of cases while preserving coordinator path for complex cases. Least privilege + practical optimization.
**Wrongs:** Full web search access (violates separation of concerns), batch all verifications (accumulated latency), proactive caching (adds complexity for unknown needs).

---

## Q11: 155K token input for 50K-capable synthesis agent
**Correct:** Modify upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning.
**Why:** Reduces token volume at source while preserving essential information. Eliminates page content and reasoning chains that inflate tokens.
**Wrongs:** Sequential batches (loses cross-source integration), intermediate summarization agent (adds latency/component), vector DB + retrieval (over-engineering).

---

## Q12: "Lost in the middle" — missing critical middle-context findings
**Correct:** Place key findings summary at beginning (primacy effect) + organize detailed results with explicit section headers.
**Why:** Mitigates "lost in the middle" phenomenon: primacy + navigation aids for middle sections.
**Wrongs:** Summarize to under 20K (loses detail), rotation of position (doesn't fix attention issue), streaming incremental processing (changes architecture unnecessarily).

---

## Q13: Corrupted PDF — error handling approach
**Correct:** Return error with context to coordinator, letting it decide how to proceed.
**Why:** Coordinator has broader context to make informed decision (skip, alternative parsing, notify user).
**Wrongs:** Auto-retry (not appropriate for corrupted file — not transient), terminate workflow (kills all progress), silent skip (hides failure).

---

## Q14: Tool naming ambiguity causing misrouting
**Correct:** Rename web search tool to `extract_web_results` and update description to reference web searches/URLs.
**Why:** Semantic overlap between `analyze_content` (web agent) and `analyze_document` (doc agent) causes coordinator misrouting. Unique, unambiguous names fix root cause.
**Wrongs:** Pre-routing classifier (adds complexity without fixing root cause), few-shot examples (probabilistic, doesn't fix tool description confusion), expand doc tool description (doesn't fix web tool ambiguity).

---

## Q15: Mixed-quality input — coverage annotations
**Correct:** Structure synthesis output with coverage annotations indicating which findings are well-supported vs which topic areas have gaps.
**Why:** Graceful degradation with transparency — preserves value of completed work while propagating uncertainty. Allows informed decisions about confidence levels.
**Wrongs:** Proceed without indicating gaps (hides uncertainty), retry before proceeding (delays output for uncertain recovery), return error (abandons completed work).

---

## Question Type Distribution

| Type | Count | Questions |
|------|-------|-----------|
| Error propagation & handling | 5 | Q1, Q2, Q7, Q13, Q15 |
| Coordinator architecture (hub-spoke) | 2 | Q4, Q6 |
| Task decomposition & partitioning | 2 | Q3, Q5 |
| Tool design & scoping (least privilege) | 3 | Q9, Q10, Q14 |
| Context & token management | 2 | Q11, Q12 |
| Conflict handling (separation of concerns) | 1 | Q8 |

## Dominant Theme: Error Propagation & Structured Context

**5 of 15 questions (33%) test error handling decisions.** The detail that matters: not just "should errors be propagated" but **how should errors be structured, categorized, and annotated**.

Key sub-themes:
- Semantic error distinction: access failure vs valid empty (Q1)
- Structured error context: type + query + partials + alternatives (Q2)
- Local recovery before escalation: transient handled locally, persistent escalated with context (Q7)
- Coverage annotations: which findings are well-supported vs which have gaps (Q15)
- Error context for informed decisions: skip vs retry vs notify (Q13)

## New Patterns NOT In Previous Debrief

1. **Error taxonomy distinction** (Q1) — Not all non-success is "failure." Access failure (timeout = retryable) is semantically different from valid empty result ("0 results" = informative outcome). The right answer distinguishes; wrong answers conflate.

2. **Coverage annotations / transparency** (Q8, Q15) — Output must indicate which findings are well-supported and which have gaps. Not just "error" or "success" but nuanced coverage metadata.

3. **Least privilege via tool interface design** (Q9, Q10) — Replace general-purpose tools with domain-specific ones that validate inputs. Scoped tools (`verify_fact` vs full web search) for specific capabilities. Makes undesired behavior impossible, not merely discouraged.

4. **Tool naming overlap as misrouting root cause** (Q14) — When two tools have semantically overlapping names/descriptions, routing becomes ambiguous. Fix: rename to eliminate ambiguity, not add proxies or classifiers.

5. **Structured data over verbose content** (Q11) — Source-level fix: have subagents return structured data (key facts, citations, scores) instead of raw content. Reduces tokens while preserving what matters.

6. **Task partitioning before delegation** (Q5) — Coordinator explicitly partitions research space before subagents run. Prevents overlap without losing parallelism.

7. **Explicit section headers for "lost in the middle"** (Q12) — Primacy effect (key findings first) + section headers for navigation in middle content. More precise than general "position-aware ordering."

8. **Local recovery before coordinator escalation** (Q7) — Subagent handles transient locally (with context of what was attempted), only escalates persistent/unresolvable.

## Pattern Cross-Reference

| Pattern | Scenario 1 | Scenario 2 | Combined |
|---------|-----------|-----------|----------|
| Context isolation (fork, explore) | 7 questions (47%) | 0 | Heavy in S1 |
| Error propagation & taxonomy | 0 | 5 questions (33%) | Heavy in S2 |
| Tool design & scoping | 2 | 3 questions | Shared |
| Coordinator/subagent architecture | 0 | 4 questions | Heavy in S2 |
| Config locations/frontmatter | 7 | 0 | Heavy in S1 |
| Plan mode vs direct | 2 | 0 | S1 only |
| Task decomposition | 0 | 2 | S2 only |
| Concrete examples/few-shot | 1 | 0 | S1 only |

**Insight:** Each scenario has a distinct "gravitational pull." Scenario 1 = **configuration-driven context management**. Scenario 2 = **error propagation & architecture patterns**. The remaining scenarios likely have their own dominant themes.
