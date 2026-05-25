# Generating Tests for CCA Study

## Philosophy

Every question is a decision-making scenario, not a trivia recall. The test-taker must choose between options that are **all plausible** to an unstudied reader but have **one optimal answer** based on Anthropic documentation.

## Question Structure

```
prompt:    A realistic scenario with trade-offs
options:   4 alternatives, all sounding reasonable
answer:    Index of optimal choice (0-3)
explain:   Structured per-option analysis using labeled sections, separated by \n\n:
           "**Correct (B):** <why optimal>\n\n**Why A is wrong:** <reason>\n\n**Why C is wrong:** <reason>\n\n**Why D is wrong:** <reason>\n\n*Docs: [Title](url)*"
```

> The HTML quiz `md()` renderer supports `**bold**`, line breaks (`\n\n`), and `` `code` `` spans — so each labeled section renders with visual separation between it.

## Rules for Writing Options

### 1. All options must be expert-plausible
Every distractor must be something a developer who knows the _general_ domain but hasn't memorized this exact doc page would plausibly choose. If a non-studier can eliminate it in under 2 seconds, rewrite it.

| Bad (obvious distractor) | Good (expert-plausible distractor) |
|--------------------------|-------------------------------------|
| "Hooks use prettier output" | "Hooks modify the system prompt before each model call, preventing guardrails from being argued away" |
| "Model selection" as a matcher option | "A case-insensitive substring match against the changed file's extension" |
| "Rotate API keys" for a config command | "Edit hook configuration interactively and reload without restarting" |
| "Deletes settings file" on exit 2 | "Blocks the change and reverts to the last known-good configuration file" |

Each distractor should be wrong for a _specific, teachable reason_ — a subtle scope error, a documented exception the test-taker might miss, or a real but misapplied behavior. Never make something wrong just by being nonsense.

### 2. Distractors should exploit common misconceptions
- **Almost-correct**: Describes a real feature but applies it to the wrong situation
- **Documented exception trap**: Correct for the general case but misses a specific exclusion (e.g., `policy_settings` can't be blocked by ConfigChange hooks)
- **Overgeneralization**: Applies a rule from event type A incorrectly to event type B
- **Plausible-but-undocumented**: Sounds like a reasonable design choice but isn't in the docs

### 3. Options must be length-balanced — correct answer must not be consistently longest

The correct answer is usually more complete and precise, so it naturally runs longer. That makes it the easiest signal to exploit. The fix: expand wrong answers with specific-sounding but false detail until all 4 options are within ~15 characters of each other.

**Expand wrong options, don't trim correct ones.** Add false event names, field paths, scope qualifiers, caveats — things that sound like they came from the same documentation page.

```
❌ BAD (length giveaway):
A) Use Haiku
B) Use Opus 4.7 with adaptive thinking and interleaved thinking auto-enabled for maximum reasoning quality
C) Use Sonnet
D) Use an older model

✅ GOOD (lengths balanced, all options look equally authoritative):
A) Use Haiku — handles tool calls well in non-streaming mode with automatic parameter inference
B) Use Opus 4.7 — handles complex tools well, but expensive and forces adaptive thinking mode
C) Use Sonnet 4.6 — balanced performance, supports both adaptive and manual thinking modes
D) Use Opus 4.6 — strong reasoning quality, but interleaved thinking is disabled in non-streaming mode
```

**After generating a batch, run a length audit:**
```js
BANK.forEach((q, i) => {
  const correctLen = q.opts[q.ans].length;
  const othersMax = q.opts.filter((_,j)=>j!==q.ans).reduce((a,o)=>Math.max(a,o.length),0);
  if (correctLen > othersMax + 15) console.log('Q'+(i+1)+': correct longer by '+(correctLen-othersMax));
});
```
Reject any question where the gap exceeds 15 characters.

## Rules for Explanations

Every explanation must cover — each part on its own labeled line:

1. **Why the correct answer is optimal** — not just "it's correct" but what specific rule, constraint, or trade-off makes it the best choice
2. **Why each distractor is wrong** — one labeled line per wrong option, naming the exact rule or documented exception it violates
3. **Docs reference** — a `*Docs: [Title](url)*` line at the end pointing to the most relevant Anthropic documentation page

### Docs reference required

Every explanation must end with a docs reference linking to the most relevant Anthropic page. Use the closest match:

| Topic | Link |
|---|---|
| Extended thinking / interleaved thinking | `https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking` |
| Tool use | `https://docs.anthropic.com/en/docs/build-with-claude/tool-use` |
| Hooks guide | `https://docs.anthropic.com/en/docs/claude-code/hooks` |
| MCP integration | `https://docs.anthropic.com/en/docs/claude-code/mcp` |
| Claude Code settings | `https://docs.anthropic.com/en/docs/claude-code/settings` |
| Message batches | `https://docs.anthropic.com/en/docs/build-with-claude/message-batches` |
| Prompt engineering | `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview` |
| Agentic loops | `https://docs.anthropic.com/en/docs/build-with-claude/agentic-loop` |
| Models overview | `https://docs.anthropic.com/en/docs/about-claude/models/overview` |

### Format

```
❌ BAD — single paragraph, letter references will break after shuffle:
"B is correct because Opus 4.7's adaptive thinking auto-enables interleaved thinking... A is wrong
because Haiku may infer missing parameters. C is wrong because while Sonnet 4.6 supports adaptive
thinking... D is wrong because Opus 4.6 manual mode does not support interleaved thinking."

✅ GOOD — labeled lines, shuffle-safe, with docs reference:
**Correct (B):** Opus 4.7's adaptive thinking auto-enables interleaved thinking, which is required
for reasoning between tool calls in this multi-step workflow.

**Why A is wrong:** Haiku may infer missing parameters — dangerous when inputs aren't fully specified.

**Why C is wrong:** Sonnet 4.6 supports adaptive thinking, but the question specifies maximum
reasoning quality for complex tools, which is Opus 4.7's strength.

**Why D is wrong:** Opus 4.6 manual mode does not support interleaved thinking, which the scenario requires.

*Docs: [Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)*
```

In the `expl` string, separate each section with `\n\n` so the `md()` renderer produces a blank line between each labeled block.

## Question Types to Use

### Scenario-Based (Preferred)
Present a realistic problem and ask what to do.

> "Your agent loops between two tools without making progress. You've already added a max_iterations cap. What should you investigate next?"

### Trade-Off Comparison
Present multiple valid approaches and ask which is optimal.

> "You need to force a specific tool while using extended thinking. Which approach is optimal?"

### Constraint-Based
Present a setup and ask what will happen or what is incompatible.

> "You set thinking: {type: 'enabled', budget_tokens: 12000} on Opus 4.7. What is the result?"

### Misconception Traps
Options that test common misunderstandings.

> "You set display: 'omitted' to reduce thinking costs. What actually happens?"

## Answer Position Distribution (Critical)

LLM-generated question banks almost always place the correct answer at `ans: 1` (position B). This is detectable and exploitable.

**Rules:**
- Vary correct answer position across A/B/C/D — roughly 25% each across the full bank
- After generating a batch, run: `grep '"ans":' file.html | sort | uniq -c` and reject if one position is >40%
- The HTML quiz template must implement `shuffleOpts(q)` so positions are re-randomized per attempt even if the bank wasn't balanced
- For exam-style files (no per-attempt shuffle), shuffle `answerIdx` intentionally during generation — don't always place correct at index 1

**Symptom to watch for:** If you open the HTML and can score 70%+ by always picking B without reading questions, the bank was generated with a position bias.

## HTML Template Requirements

All HTML quiz artifacts must implement:

1. **Inline markdown rendering** (`md()` function) applied to all user-visible text:
   - Question prompt
   - Option text
   - Explanation text
   - Use `` `code` `` → `<code>` styling with monospace font and subtle background
   - Never use raw `escapeHtml()` or plain string insertion for question content
   - The `md()` renderer supports `**bold**`, line breaks (`\n\n`), and `` `code` `` spans — the structured per-option explanation format (labeled `**Correct:**` / `**Why X is wrong:**` blocks separated by `\n\n`) will render with visual separation between each section

2. **Answer shuffling** applied at display time, not just at bank creation:
   - Per-attempt shuffle (`shuffleOpts`) in quiz mode
   - `buildPool()` in exam mode (shuffle each question's options before storing `correctIdx`)
   - Explanation text must not reference the pre-shuffle letter (strip or avoid `"B is correct..."`)

   > **Final exam note (`cca_generate_exam_html.py`):** The final exam is a **sequential (non-rotating) exam** — all questions are shown on every attempt, with no random subset selection. It uses `mdInline()` instead of `md()` for markdown rendering, which produces the same output. Options are shuffled once at pool-build time via `buildPool()`.

3. **`<code>` CSS** must be included:
   ```css
   code {
     font-family: ui-monospace, monospace;
     background: rgba(96,165,250,0.12);
     color: #93c5fd;
     padding: 0.1em 0.38em;
     border-radius: 5px;
     font-size: 0.855em;
     border: 1px solid rgba(96,165,250,0.2);
   }
   ```

## Contrast & Accessibility

- Body text: minimum `#d4d4e0` on `#0a0a0f` (7:1 contrast ratio)
- Dim text: minimum `#9ca3af` (4.5:1)
- Option borders: minimum `rgba(148,163,184,0.25)` for unselected, `rgba(56,189,248,0.5)` for selected
- Correct/wrong states must be distinguishable without color (checkmark vs X, or border style)
- Font size: minimum 16px for body, 14px for secondary text

## Topic Coverage

Each domain should have 30+ questions covering:
- Definitions (20%)
- Best practices (30%)
- Trade-off decisions (30%)
- Edge cases and constraints (20%)

**Final exam bank:** Each module bank must have exactly **30 questions** to match the default `--per-module 30` setting. To expand to 40 questions per module, update `build_module_banks.py` to set `TARGET_PER_MODULE = 40` and re-run `python tools/build_module_banks.py` before regenerating the exam.

## Question Bank Source Format

This format applies to **all bank types**: module banks, full-rotation concept banks, and block-plan drills.

```markdown
## Question N
[Scenario prompt — 2-4 sentences, specific technical context]

A) [Option text]
B) [Option text]
C) [Option text]
D) [Option text]

<details>
<summary>Answer</summary>

**X)** Why the correct answer is optimal — 1-2 sentences. A is wrong because [specific rule violated]. B is wrong because [specific reason]. C is wrong because [specific reason]. (source: [Anthropic docs page name])

</details>

---
```

**Critical rules:**
- `**X)**` prefix — correct letter in pre-shuffle order; stripped by parser to set `ans` index
- `(source: ...)` suffix — stripped by parser, shown as docs reference on results screen
- **Every wrong option must get its own sentence** using `[letter] is wrong because` — this exact pattern is what the renderer (`buildVerboseExplanation`) splits on to create per-option blocks
- Split triggers recognized: `. A is wrong`, `. B is wrong`, `. C is wrong`, `. D is wrong`, `. Option A`, etc.
- Do NOT use the labeled heading format (`**Why A is wrong:**`) — the renderer does not split on this
- Do NOT use newlines inside `<details>` — the parser normalizes whitespace; structure is added at render time
- Letters must be **pre-shuffle positions** — renderer remaps to post-shuffle display letters via `origToNew`

**What renders as (per-option blocks with dividers):**
```
Why the correct answer is optimal.
────────────────────────────────
A is wrong because [specific rule violated].
────────────────────────────────
B is wrong because [specific reason].
────────────────────────────────
C is wrong because [specific reason].
```

**Known debt:** The four full-rotation concept banks (`practice-tests/concept-banks/concept-*.md`) were converted from old HTML quizzes with narrative single-paragraph explanations — they lack `. X is wrong` split triggers and render as single blocks. Their explanations must be rewritten to use this format before they match module bank quality.

## Do NOT Overfit to Real-Exam Scenarios

When the source of questions is real exam analysis files (e.g., `practice-tests/real-exam-questions/`):

- Write questions that test the **same concepts** but with completely different scenario domains, entities, and structural arc
- Never re-skin a real exam question by only changing the company name, sector, or surface nouns — if the question structure, the trap, and the correct reasoning path are the same, it's still the same question
- A good rewrite changes: the industry/domain, the specific tool or constraint in play, and the order in which information is revealed — while preserving the underlying tested concept (e.g., "when to use streaming vs. batching" stays the concept, but the scenario becomes a genomics pipeline instead of a customer-support queue)
- If you cannot write a meaningfully different scenario, write a question that tests the same concept from a different angle (constraint-based vs. scenario-based, or trade-off vs. misconception-trap)

## Source Material

All questions must be traceable to:
- Official Anthropic documentation
- Engineering blog posts
- API reference
- CCA study guide

Mark each question with a `source` tag for review.
