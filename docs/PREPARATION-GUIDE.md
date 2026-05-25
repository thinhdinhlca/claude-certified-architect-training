# How I Prepared for the Claude Certified Architect Exam

Thought I'd write down my approach in case it helps anyone else preparing for this.

---

## The mindset shift

I initially approached this like any other certification — read the docs, make some notes, take the test. That lasted about one day before I realized this exam is different. It's not testing whether you've memorized API parameters. Every question is a **decision-making scenario**: "Here's a system with a real problem. What do you do?"

So I stopped trying to study and started trying to *build*. Specifically, I had Claude build me a study system. Everything that follows was generated through prompts. I never wrote a single quiz question or note by hand.

---

## What I actually did

### 1. Made Claude build me quizzes

I realized passive reading was useless for this exam. I needed to practice making trade-off decisions under time pressure. So I had Claude generate self-contained HTML quiz files — one per domain. Open in any browser, no internet needed.

The format: 30 questions per bank, 20 drawn randomly per attempt. Questions and answer order shuffled every time so I couldn't memorize positions. Each question presents a realistic scenario with 4 options that all sound plausible to someone who half-knows the material — the kind of distractor that exploits a real misconception.

The killer feature was localStorage persistence. The quiz remembers how many perfect passes I've achieved and tracks which topics I keep getting wrong, even across browser restarts. I set the bar at 2 perfect runs per domain before moving on.

**The prompt that started it:** *"Build me an HTML quiz for CCA Domain 1. 30 scenario-based questions with 4 plausible options each. Wrong answers should target specific misconceptions. Track perfect passes in localStorage. Make explanations shuffle-proof."*

Then I iterated: *"Question 8 has an obviously wrong distractor — rewrite it. Question 14's correct answer is the longest — rebalance. Question 22's explanation references 'option B' which breaks when shuffled."*

Each quiz took about an hour of back-and-forth with Claude, and every round of fixes made me internalize the material more deeply than reading ever would.

### 2. Built an Obsidian vault as my external brain

I use Obsidian for everything, so this was natural. The structure is simple:

- **Daily notes** — one per study session. What I read, which quiz I took, my score, the specific topics I missed, and 3-5 flashcards generated from my mistakes.
- **Domain notes** — one per domain. Not definitions. Decision rules. "When do you use programmatic hooks vs prompt guidance?" "What's the actual tradeoff between plan mode and direct execution?" The kind of thing that shows up in exam questions.
- **Playbooks** — repeatable procedures. My retest protocol, my full-mock-exam protocol.

The rule I enforced: **every claim must link to a source.** No floating opinions. Every decision rule, every anti-pattern, every flashcard traces back to either an Anthropic docs page or a specific quiz question I got wrong. This matters because when you're reviewing at 10 PM and you see "use stop_reason, not natural language parsing," you want to click through and re-read *why*.

**The prompt that built this:** *"Create an Obsidian vault for CCA study. Daily notes in one folder, domain notes in another, playbooks in a third. The daily note template must include: focus, sources read, quiz score, weak areas, and auto-generated flashcards. Every claim in domain notes must link to a source URL."*

### 3. Designed a daily protocol with zero decision fatigue

The biggest enemy of consistent studying is the moment you sit down and think "what should I do today?" If you have to decide, you've already lost momentum.

My solution: a JSON file that maps every calendar date from May 9 to June 19 to a specific focus, a reading list, and a test command. When study time arrives, I run one command that tells me exactly what to read and which quiz to take. No choices, no scrolling, no deciding.

Time blocks: 1 hour reading, 1 hour testing on weekdays. 2 hours reading, 1 hour review, 2 hours testing on weekends.

**The prompt:** *"I study CCA weekdays 8-10 PM, weekends 9-11 AM and 8-10 PM. Generate a daily plan from May 9 to June 19 covering all 5 domains, with specific readings and test sources for each day. Output as a date-indexed JSON file."*

### 4. Accelerated when I was ready

The original plan was 12 weeks. After completing Week 1's material in 2 days, I realized the pace was too conservative. I had Claude re-plan from 12 weeks to 6 weeks with a buffer, shifting all dates forward and condensing where possible. The key insight: **don't follow a schedule rigidly — follow your actual progress.** If a domain clicks in 2 days instead of 7, move on. If something isn't sticking, slow down and drill.

---

## What I learned along the way

### The anti-patterns are everything

At least a third of exam questions test whether you can spot a wrong approach. These 10 anti-patterns came up over and over:

1. Parsing natural language instead of checking `stop_reason`
2. Using iteration caps as the primary loop control
3. Putting critical business rules in prompts instead of programmatic hooks
4. Trusting a model's self-reported confidence
5. Escalating based on customer sentiment alone
6. Returning generic error messages
7. Silently suppressing errors
8. Giving every agent access to too many tools
9. Having the same session review its own code
10. Measuring aggregate accuracy while ignoring per-category failures

Once I had these memorized, many questions became straightforward: three options are variations on these anti-patterns, one is the correct approach.

### Decision frameworks beat definitions

The exam never asks "what is a hook?" It asks "should you use a hook or a prompt for this situation?" I built a reference table of common trade-offs that turned out to be the most useful study artifact:

| Situation | Right call | Wrong call |
|-----------|-----------|------------|
| Financial/safety risk | Programmatic hooks | Prompt instructions |
| Multi-file refactor | Plan mode | Direct execution |
| Pre-merge checks | Synchronous API | Batch API |
| Error handling | Structured context with retry flag | Generic "operation failed" |
| Large PR review | Multi-pass (per-file then integration) | Single-pass |

### The quiz-generation process IS the studying

This was the biggest revelation. Having Claude generate quiz questions was more valuable than actually taking the quizzes. Every time I said "that distractor isn't plausible enough" or "the correct answer is too obvious because it's longer," I was forced to understand the material at a deeper level. You can't critique a wrong answer without knowing exactly why it's wrong.

### Quiz Question Construction Patterns (from real exam analysis)

After analyzing real exam questions from Scenario 1 (Code Generation with Claude Code), these patterns emerged:

**1. Plan mode vs direct execution (decision framework questions)**
Framing: "You have task X. Multiple valid paths, ambiguous requirements. How to approach?"
- Correct: Plan mode for multi-path, architectural, ambiguous requirements
- Wrong: Direct execution prematurely, picking one path without exploring
- Signal words: "fundamentally different approaches," "without specifying which," "architectural restructuring"

**2. Multi-symptom config questions**
Framing: "Your [skill/command/system] has 2-3 distinct issues. What single approach fixes all?"
- Correct: Combines multiple config features (argument-hint + context:fork + allowed-tools)
- Wrong: Prompt-based instructions (probabilistic) or solutions that address only one symptom
- Tests: Can you match the right frontmatter/feature to each symptom?

**3. Context pollution questions (dominant theme — 47% of questions)**
Framing: "X generates verbose output / uses outdated context / influences subsequent work."
- Correct: `context: fork`, Explore subagent, skills on-demand, `.claude/rules/` glob patterns
- Wrong: Model switching, output compression, prompt instructions, splitting into more skills
- Tests: "What's the right isolation mechanism?" Is it frontmatter, subagent type, or conditional loading?

**4. Config location questions (project vs user scope)**
Framing: "New teammate doesn't get X / inconsistent team behavior / want all devs to have it."
- Correct: Project-scoped location (`.claude/CLAUDE.md`, `.claude/commands/`, `.claude/skills/`, `.mcp.json`)
- Wrong: User-scoped location (`~/.claude/...`) when team consistency is needed
- Key: Project scope = version-controlled, shared. User scope = personal, not shared.

**5. On-demand vs always-loaded context**
Framing: "X is only needed for task Y, not for tasks A, B, C."
- Correct: Skill (on-demand invocation) for task-specific context, CLAUDE.md for always-applied standards
- Wrong: Everything in CLAUDE.md (bloats every session), or everything as skills (standards not automatic)
- Decision rule: Always-need-it = CLAUDE.md. Sometimes-need-it = Skill. By-file-path = `.claude/rules/` glob.

**6. Concrete examples as the fix for ambiguity**
Framing: "Prose requirements keep getting misinterpreted. What's the most effective approach?"
- Correct: 2-3 concrete input-output examples (few-shot)
- Wrong: More precise prose, JSON schema validation, asking Claude to explain itself
- Signal: The problem is *interpretation ambiguity*, not *validation* or *clarity*

**7. Skill customization without affecting team**
Framing: "One developer wants different behavior for team skill. How?"
- Correct: Different name in `~/.claude/skills/`
- Wrong: Same name (project takes precedence), modifying team skill, conditional logic
- Key: Same-name personal skills are overridden by project skills

### Distractor Design Rules (from real exam)

1. **Similar length** — All 4 options roughly same verbosity. No "longest is correct" heuristic.
2. **No gimmicks** — Never "all of the above," "none of the above," or extreme language.
3. **Plausible but flawed** — Each wrong answer targets a real misconception, not random nonsense.
4. **Constraint-negated** — A specific detail in the question makes the distractor wrong.
5. **Mixes levels** — Some distractors are correct for a *different* scenario; wrong here because of constraints.
6. **Prompt-based as a distractor** — "Add instructions to the prompt" is often wrong when deterministic config (hooks, frontmatter, allowed-tools) is the correct answer. Prompt instructions are probabilistic; config is deterministic.

### Explanation Rules

Every answer explanation must cover:
1. Why the correct answer is correct (mechanism, not just assertion)
2. Why EACH of the three distractors is wrong (specific reason per distractor)
3. The principle or decision framework at work

### Scenario-Type Patterns (from real exam analysis)

**Scenario 1 — Code Generation with Claude Code:** Dominated by configuration-driven context management (47% of questions). Tests: CLAUDE.md hierarchy, skills frontmatter, .claude/rules/ glob patterns, MCP config, commands location, plan mode. Focus: "Where does config go and how does it control Claude's behavior?"

**Scenario 2 — Multi-Agent Research System:** Dominated by error propagation & architecture (33% of questions). Tests: structured error context, error taxonomy, coverage annotations, least-privilege tool design, task partitioning, local recovery before escalation, tool naming clarity. Focus: "How does information flow between agents and how are failures handled?"

### Multi-Agent Scenario Patterns (New)

**8. Error taxonomy questions**
Framing: "Agent returns outcome X and outcome Y. How should you propagate them?"
- Correct: Distinguish access failures (timeout = retryable) from valid empty results ("0 results" = informative)
- Wrong: Aggregate into single metric, treat both as failures, hide transient/permanent distinction
- Tests: Can you categorize errors semantically, not just surface-level?

**9. Coverage annotation questions**
Framing: "Output is incomplete due to partial source availability. How to handle?"
- Correct: Annotate which findings are well-supported vs which have gaps due to unavailable sources
- Wrong: Proceed without indicating gaps, retry everything, return error abandoning all work
- Tests: Graceful degradation with transparency. Preserve completed work while propagating uncertainty.

**10. Least privilege tool design (interface level)**
Framing: "Agent X is using tool Y to do things it shouldn't. How to fix?"
- Correct: Replace general tool with domain-specific, input-validating tool (fetch_url → load_document)
- Wrong: Prompt instructions (probabilistic), domain filtering (whack-a-mole), routing through coordinator (latency)
- Tests: Make undesired behavior structurally impossible, not merely discouraged.

**11. Scoped capabilities for efficiency**
Framing: "Agent frequently needs simple X but current process adds round-trips. 85% are simple, 15% complex."
- Correct: Give scoped tool for 85% simple case; 15% complex still goes through coordinator
- Wrong: Full access (violates separation), batch everything (latency), all-or-nothing (rigid)
- Tests: Balance least privilege with practical optimization. Partition by complexity.

**12. Tool naming ambiguity**
Framing: "Agent X is getting tasks meant for Agent Y. Both have similar tool names."
- Correct: Rename tools to be unique and scope-specific (analyze_content → extract_web_results)
- Wrong: Pre-routing classifiers, few-shot examples, expanding descriptions (doesn't fix name overlap)
- Tests: Tool names must be unambiguous. Semantic overlap in names causes routing confusion at the coordinator level.

**13. Structured output over verbose content**
Framing: "Subagents produce verbose output (page text, reasoning chains) that exceeds synthesis capacity."
- Correct: Return structured data (key facts, citations, relevance scores) — cut volume at source
- Wrong: Sequential batching (loses integration), intermediate summarizer (adds latency/component), vector DB (over-engineered)
- Tests: Prevent token problems at the source, not by adding more components.

**14. Task partitioning before delegation**
Framing: "Parallel subagents produce overlapping findings, doubling tokens without expanding coverage."
- Correct: Coordinator partitions research space before delegation (distinct subtopics/source types per agent)
- Wrong: Deduplicate after (token waste), shared state (complexity), switch to sequential (loses parallelism)
- Tests: Proactive partitioning prevents duplicate work. Reactive dedup is a band-aid.

**15. Local recovery before escalation**
Framing: "Routine errors cause excessive coordinator involvement. How to improve?"
- Correct: Subagent handles transient locally, escalates only persistent with context of attempts + partial results
- Wrong: Coordinator pre-validates (burden shift), dedicated error agent (complexity), always return success (hides failures)
- Tests: Handle at lowest capable level. Don't reverse the delegation model.

### CI/CD Scenario Patterns (from Scenario 3)

**16. Batch vs synchronous API decision framework**
Framing: "You have workflows X (blocking, dev waiting) and Y (overnight, scheduled). Which uses batch?"
- Correct: Blocking/pre-merge → synchronous. Deferred/overnight → batch (50% savings).
- Signal words: "blocks merging until complete" = sync. "generated overnight" = batch.
- Key trap: Iterative tool-calling workflows CANNOT use batch even if latency-tolerant. Batch = fire-and-forget; no mid-request tool interception possible.

**17. False positive trust cascading**
Framing: "Category A has 8% FP rate. Category B has 52%. Developers dismiss all findings."
- Correct: Temporarily disable high-FP categories; run only high-precision while improving prompts.
- Wrong: Uniform strictness (degrades accurate ones), confidence scores (devs already distrust), gradual few-shot (trust erodes during improvement).
- Tests: High-FP noise corrupts trust in low-FP signal. Fix per-category, not uniformly.

**18. Inline reasoning for triage without filtering**
Framing: "Many findings, bottleneck is clicking each to read reasoning. Filtering is rejected by stakeholders."
- Correct: Include reasoning + confidence inline so devs evaluate without clicks.
- Wrong: Post-process filters, high-confidence-only surfacing, tiered review.
- Tests: Presentation optimization when filtering is not an option.

**19. Prior review findings as context for re-review**
Framing: "After fix commits, review generates duplicates of previously addressed issues."
- Correct: Include prior review findings in context; Claude distinguishes new from addressed.
- Wrong: Scope restriction (misses cross-commit context), skip intermediate reviews, post-filtering.
- Tests: Leverage Claude's reasoning to avoid redundant feedback, not heuristic filtering.

**20. CLI flags for CI/CD automation**
Framing: "Pipeline hangs waiting for input / needs structured parseable output."
- Correct: `-p` for non-interactive mode (exit without waiting). `--output-format json` + `--json-schema` for structured output enforcement.
- Wrong: Fake env vars (`CLAUDE_HEADLESS`), /dev/null redirect, fake flags (`--batch`), prompt-based format instructions.
- Tests: Exact knowledge of CI/CD-relevant CLI flags. Must know correct names — the exam uses fake flag/env names as distractors.

### Customer Support Scenario Patterns (from Scenario 4)

**21. Tool description improvement as first diagnostic step**
Framing: "Agent consistently picks wrong tool (e.g., get_customer instead of lookup_order). What to examine first?"
- Correct: Review tool descriptions — expand with input formats, example queries, edge cases, boundaries vs similar tools.
- Wrong: Few-shot exhaustively, pre-processing classifier, reduce tools. Root cause before complex fixes.
- Tests: Tool descriptions are the primary mechanism. Fix them before adding architectural layers.

**22. ⚠️ Few-shot vs Self-Critique decision boundary (TRAP)**
Framing: "Output inconsistently missing elements. The specific gaps vary by case."
- Signal for few-shot: Consistent, predictable gaps ("always missing policy detail").
- Signal for self-critique (evaluator-optimizer): "Specific context gaps vary by case" — gaps aren't predictable.
- Correct: Self-critique step evaluating draft against criteria (policy context, timelines, next steps).
- Wrong: Few-shot examples (covers common patterns, misses variable gaps).
- Tests: Don't reflexively pick few-shot. When gaps are unpredictable, self-evaluation beats pattern examples.

**23. ⚠️ Few-shot vs Preprocessing decision boundary (TRAP)**
Framing: "Single-concern 94% accuracy. Multi-concern drops to 58%."
- Signal for few-shot: High single-concern baseline → just needs multi-concern pattern guidance.
- Signal for preprocessing: Fundamental architecture limitation, not just guidance gap.
- Correct: Few-shot examples showing multi-concern reasoning and tool sequencing.
- Wrong: Separate preprocessing model call (over-engineering when baseline is already strong).
- Tests: When baseline is strong, don't add architectural layers. Add pattern guidance.

**24. Persistent "case facts" block vs better summarization**
Framing: "Summarization loses precise details (amounts, dates). Agent gives wrong values."
- Correct: Extract transactional facts into persistent "case facts" block outside summarized history.
- Wrong: Increase threshold (delays loss), revise summarization prompt (still lossy), external retrieval (complex).
- Tests: Summarization is inherently lossy for precision. Persist critical facts in structured blocks.

**25. Programmatic prerequisites for mandatory tool sequences**
Framing: "Agent skips verification step, causing misidentified accounts and incorrect refunds."
- Correct: Programmatic prerequisite blocking downstream tools until prerequisite tool returns verified result.
- Wrong: Few-shot, prompt instructions (both probabilistic). Deterministic guarantee needed for financial/safety.
- Tests: When step X must always precede step Y, enforce it programmatically, not with prompts.

**26. Keyword-sensitive prompt steering diagnosis**
Framing: "Selection varies by keyword ('account' vs no keyword) even though tool descriptions are fine."
- Correct: System prompt contains keyword-sensitive instructions creating unintended routing.
- Wrong: Fine-tuning, base training blame, negative tool description examples.
- Tests: Diagnose root cause systematically. Descriptions fine + keyword pattern = suspect prompt instructions.

**27. User disambiguation over probabilistic heuristics**
Framing: "Multi-match customer lookup has 15% error rate from wrong selection."
- Correct: Ask user for additional identifier (email, phone, order number).
- Wrong: Confidence scoring (anti-pattern), single-return ranking (hides ambiguity), conversational inference (probabilistic).
- Tests: One extra turn is cheaper than 15% wrong-customer error rate. User has definitive knowledge.

**28. Tool batching via prompt (not architecture)**
Framing: "4+ round-trips. Claude requests get_customer and lookup_order in separate turns when both are needed."
- Correct: Prompt Claude to batch related tool requests per turn, return all results together.
- Wrong: Speculative execution (calls unnecessary tools), increase max_tokens (more space ≠ batching), composite tools (maintenance burden).
- Tests: Leverage Claude's native multi-tool capability before adding architectural complexity.

### Retesting immediately matters

My protocol was: if I scored below 1000 on a quiz, I retook it *immediately, same session*. Not "I'll review and try tomorrow." The mistakes are fresh, the reasoning is still accessible, and the correction sticks better when applied right away.

---

## How you can do this

You don't need my files. You need to **ask your agent to build your own**. Here's the playbook:

**Session 1 — Infrastructure:**
*"I'm preparing for the Claude Certified Architect exam. Build me a self-contained HTML quiz for Domain 1 with 30 scenario-based questions, localStorage pass tracking, and shuffle-proof explanations. Also set up an Obsidian vault with daily note and domain note templates."*

**Ongoing — Content (one domain per week):**
*"Read the Anthropic docs on [domain]. Generate a 30-question HTML quiz using the same template. For each question: 4 plausible options, one optimal answer, and an explanation covering why each distractor is wrong. Create the corresponding domain note in Obsidian with decision rules and anti-patterns."*

**Every session:**
*"Today I studied [topic]. I scored [X] on the quiz and missed questions about [topics]. Update my Obsidian daily note with today's focus, sources, score, weak areas, and 3-5 flashcards from my mistakes."*

**When you're stuck:**
*"I keep getting questions about [concept] wrong. Read the Anthropic doc on this and explain the concept to me like I'm a developer who's never used it. Then give me 5 scenario questions targeting my specific gap."*

---

## The bottom line

The exam tests whether you can make good decisions about Claude-based systems. The best preparation isn't reading documentation — it's repeatedly encountering decision scenarios, getting them wrong, understanding why, and trying again until the right call becomes instinct. An agent can build you the machinery for this. You just need to show up and do the reps.

*— Thinh, May 2026*
