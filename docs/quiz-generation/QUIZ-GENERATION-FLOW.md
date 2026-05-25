# CCA HTML Quiz Generation Flow

**Last updated:** 2026-05-24  
**Status:** Standardized across module quizzes and concept quizzes via `cca_generate_module_quiz.py`

---

## Quiz Inventory (as of 2026-05-24)

### ✅ Generated — Module quizzes (30Q / 20 per attempt / 60 min)

| File | Source bank | CCA Scenario |
|------|-------------|--------------|
| `cca-customer-support-quiz.html` | `module-banks/module-customer-support.md` | A |
| `cca-code-generation-quiz.html` | `module-banks/module-code-generation.md` | B |
| `cca-multi-agent-research-quiz.html` | `module-banks/module-multi-agent-research.md` | C |
| `cca-developer-productivity-quiz.html` | `module-banks/module-developer-productivity.md` | D |
| `cca-ci-cd-quiz.html` | `module-banks/module-ci-cd.md` | E |
| `cca-structured-extraction-quiz.html` | `module-banks/module-structured-extraction.md` | F |

### ✅ Generated — Concept quizzes (30Q / 20 per attempt / 60 min)

| File | Source bank | Topic |
|------|-------------|-------|
| `cca-agentic-loops-quiz.html` | `concept-banks/concept-agentic-loops.md` | Agentic control flow, stop conditions, tool loops |
| `cca-mcp-quiz.html` | `concept-banks/concept-mcp.md` | MCP architecture, transports, primitives, lifecycle |
| `cca-tool-use-quiz.html` | `concept-banks/concept-tool-use.md` | Tool schema, tool_choice, extended thinking |
| `cca-hooks-quiz.html` | `concept-banks/concept-hooks.md` | Hook lifecycle, matchers, decision control |
| `cca-context-isolation-quiz.html` | `concept-banks/concept-context-isolation.md` | `context: fork`, CLAUDE.md vs Skills vs `.claude/rules/` |
| `cca-error-propagation-quiz.html` | `concept-banks/concept-error-propagation.md` | Error taxonomy, local recovery, structured errors |
| `cca-batch-vs-sync-quiz.html` | `concept-banks/concept-batch-vs-sync.md` | Batch API incompatibilities, polling, CI mode |
| `cca-few-shot-patterns-quiz.html` | `concept-banks/concept-few-shot-patterns.md` | Few-shot vs self-critique vs preprocessing |

### ✅ Generated — Block-plan drills (10Q / 10 per attempt / 25 min)

| File | Source bank | Topic |
|------|-------------|-------|
| `cca-agentic-loops-drill-quiz.html` | `test-01-agentic-loops.md` | Agentic loop control flow, stop_reason |
| `cca-multi-agent-systems-quiz.html` | `test-02-multi-agent.md` | Multi-agent orchestration patterns |
| `cca-hooks-workflows-drill-quiz.html` | `test-03-hooks-workflows.md` | Hooks, programmatic prerequisites |
| `cca-tool-design-mcp-drill-quiz.html` | `test-04-tool-design-mcp.md` | Tool naming, MCP primitives |
| `cca-claude-code-config-quiz.html` | `test-05-claude-code-config.md` | Claude Code config scope |
| `cca-plan-mode-cicd-quiz.html` | `test-06-plan-mode-cicd.md` | Plan mode, CI/CD integration |
| `cca-prompt-engineering-quiz.html` | `test-07-prompt-engineering.md` | Prompt engineering patterns |
| `cca-validation-multipass-quiz.html` | `test-08-validation-multipass.md` | Validation and multi-pass flows |
| `cca-context-reliability-quiz.html` | `test-09-context-reliability.md` | Context window management |
| `cca-advanced-context-quiz.html` | `test-10-advanced-context.md` | Advanced context strategies |

### ✅ Generated — Final exams

| File | Source | Questions |
|------|--------|-----------|
| `cca-prep-exam.html` | All 6 module banks | 180Q sequential |
| `cca-scenario-exam.html` | Rotating subset | 60Q timed |

---

### ✅ All source files now have HTML quizzes

### ❌ Missing — Concept banks for high-frequency exam patterns

From real-exam analysis (`docs/exam-debrief-1.md`), these cross-cutting patterns appear in 27–47% of questions but have no focused concept bank or drill:

| Concept area | Exam frequency | Notes |
|---|---|---|
| Context isolation (`context: fork`, skills on-demand, `.claude/rules/`) | ~47% of Scenario 1 | Needs a 30Q concept bank |
| Error propagation taxonomy | ~33% of Scenario 2 | Needs a 30Q concept bank |
| Batch vs sync API decision rules | ~27% of Scenario 3 | Needs a 30Q concept bank |
| Few-shot vs self-critique vs preprocessing | Calendar block 2026-06-12/16/18 | Needs a 10Q targeted drill |

These are the highest-leverage gaps before the exam.

---

## The Flow

### 0. Playbook Triggers
- **When reading is finished for a topic/day:** generate or refresh the HTML quiz artifact for that topic before taking the timed run.
- **When pass criteria is met:** record a pass checkpoint in repo logs so next sessions can resume from the right point.

### 1. Source Material

Two types of question banks feed the generator:

| Bank type | Location | Questions | Use |
|-----------|----------|-----------|-----|
| Module banks (6 scenario modules) | `practice-tests/module-banks/module-{id}.md` | 30 each | Wide scenario coverage per CCA module |
| Concept banks (4 full rotation) | `practice-tests/concept-banks/concept-{id}.md` | 30 each | Narrow drill: Agentic Loops, MCP, Tool Use, Hooks |
| Concept drills (7 block-plan drills) | `practice-tests/test-{NN}-{topic}.md` | 10 each | Block plan drill: Error Propagation, Config Scope, etc. |

All formats use: `## Question N`, `A) / B) / C) / D)`, `<details><summary>Answer</summary>`.

### 2. Question Standards (from `GENERATING-TESTS.md`)
| Rule | Description |
|------|-------------|
| Decision scenarios | Questions must be applied scenarios, not trivia recall |
| Plausible distractors | Wrong answers should sound reasonable to someone who misunderstood the concept |
| Parallel structure | All 4 options should be similar in length and grammatical structure |
| No correct-answer-is-longest | Balance answer lengths — correct answer should not consistently be the longest option |
| Per-option explanations | `expl` must address every wrong option by letter: "A is wrong because..." — bare letter references are REQUIRED for the renderer to split segments |
| Source reference required | `expl` must end with `(source: Anthropic docs page name)` |
| Unique distractors | All 4 options must be clearly distinct — no two options saying the same thing in different words |

### 3. HTML Quiz Template

All quizzes are generated by `tools/cca_generate_module_quiz.py` using one unified template:

| Element | Standard |
|---------|----------|
| Bank size | 30Q full rotation; 10Q for block-plan drills |
| Per attempt | 20 (30Q banks) or 10 (10Q banks) |
| Pass threshold | 2 perfect runs (1000/1000) |
| Timer | 60 min (30Q) or 25 min (10Q) |
| Pass tracking | localStorage (`cca_{module_id}_pass_count`) |
| Wrong answer tracking | localStorage (`cca_{module_id}_wrong_answers`) |
| Nav dots | Green = correct answer, Red = wrong answer (post-answer) |
| Keyboard | `1-4` / `A-D` select, `Enter` advance, `←/→` navigate (Arrow keys do NOT select — `e.key.length === 1` guard) |
| Theme | Dark, accent color varies per module |
| Shuffle-safe letters | `origToNew` mapping remaps explanation letter references to post-shuffle positions |
| Dependencies | Zero — self-contained HTML file, no build step |

**Bank sizes by quiz type:**

| Quiz type | Bank size | Per attempt | Timer | Generator flag |
|-----------|-----------|-------------|-------|----------------|
| Module quizzes (6 scenario) | 30 | 20 | 60 min | default |
| Concept quizzes (4 full rotation) | 30 | 20 | 60 min | `--concepts-only` |
| Block-plan drills (7 narrow) | 10 | 10 | 25 min | `--concepts-only` |
| Final exam | 180 (all shown) | All 180 | 150 min | `cca_generate_exam_html.py` |

### 4. Accent Color Scheme

| Module | Accent | Hex |
|--------|--------|-----|
| customer-support | Violet | `#a78bfa` |
| code-generation | Blue | `#60a5fa` |
| multi-agent-research | Emerald | `#34d399` |
| developer-productivity | Orange | `#fb923c` |
| ci-cd | Rose | `#f43f5e` |
| structured-extraction | Amber | `#fbbf24` |
| agentic-loops | Sky | `#38bdf8` |
| mcp | Teal | `#2dd4bf` |
| tool-use | Amber | `#fbbf24` |
| hooks | Purple | `#c084fc` |
| multi-agent-systems | Emerald | `#34d399` |
| claude-code-config | Blue | `#60a5fa` |
| plan-mode-cicd | Rose | `#f43f5e` |
| prompt-engineering | Orange | `#fb923c` |
| validation-multipass | Violet | `#a78bfa` |
| context-reliability | Teal | `#2dd4bf` |
| advanced-context | Pink | `#f472b6` |

### 5. Generation Commands

```bash
# All 6 module quizzes
python tools/cca_generate_module_quiz.py --modules-only

# All 11 concept quizzes (4 full rotation + 7 block drills)
python tools/cca_generate_module_quiz.py --concepts-only

# All 17 quizzes at once
python tools/cca_generate_module_quiz.py

# Single quiz by ID
python tools/cca_generate_module_quiz.py --module hooks

# Final exam (180Q)
python tools/cca_generate_exam_html.py
```

### 6. Adding a New Concept Bank
1. Write questions to `practice-tests/concept-banks/concept-{id}.md` (30Q) or `practice-tests/test-NN-{topic}.md` (10Q)
2. Use the standard explanation format (see below — per-option inline, not labeled headings)
3. Add an entry to `CONCEPT_MODULES` in `tools/cca_generate_module_quiz.py`
4. Add accent color to `ACCENT_COLORS` and tags to `DOMAIN_TAGS`
5. Run `python tools/cca_generate_module_quiz.py --module {id}`

### Module Quiz Generation

Generates HTML quiz files from module learning banks. Uses the same template and standards as topic quizzes (30 bank / 20 per attempt / 60 min / 1000 pass threshold × 2).

**Source:** `practice-tests/module-banks/module-{id}.md`  
**Generator:** `tools/cca_generate_module_quiz.py`  
**Output:** `quizzes/cca-{module-id}-quiz.html`

```bash
# Generate all 6 module quizzes
python tools/cca_generate_module_quiz.py

# Generate a single module quiz
python tools/cca_generate_module_quiz.py --module {id}
```

**Output files (all 6):**
- `quizzes/cca-customer-support-quiz.html`
- `quizzes/cca-code-generation-quiz.html`
- `quizzes/cca-multi-agent-research-quiz.html`
- `quizzes/cca-developer-productivity-quiz.html`
- `quizzes/cca-ci-cd-quiz.html`
- `quizzes/cca-structured-extraction-quiz.html`

**Module accent colors:**

| Module | Accent | Hex |
|--------|--------|-----|
| customer-support | Violet | `#a78bfa` |
| code-generation | Blue | `#60a5fa` |
| multi-agent-research | Emerald | `#34d399` |
| developer-productivity | Orange | `#fb923c` |
| ci-cd | Rose | `#f43f5e` |
| structured-extraction | Amber | `#fbbf24` |

---

### Final Exam Generation

Generates a full-length sequential exam from all 6 module banks. Unlike quiz mode, the final exam shows **all questions without rotation** — every question appears on every attempt.

**Generator:** `tools/cca_generate_exam_html.py`  
**Output:** `quizzes/cca-prep-exam.html`  
**Default:** 6 modules × 30 questions = **180 questions**, 150-minute timer  
**Pass threshold:** 720 / 1000 (72%)

```bash
# Default: all 6 modules, 30 questions each, 150-minute timer
python tools/cca_generate_exam_html.py

# All modules explicitly
python tools/cca_generate_exam_html.py --all-modules

# Single module only
python tools/cca_generate_exam_html.py --module-id customer-support

# Custom questions per module and timer
python tools/cca_generate_exam_html.py --per-module 40 --timed-minutes 200

# Reproducible shuffle
python tools/cca_generate_exam_html.py --seed 42
```

**To expand to 40 questions per module:**
1. Update `tools/build_module_banks.py`: set `TARGET_PER_MODULE = 40`
2. Re-run: `python tools/build_module_banks.py`
3. Re-generate: `python tools/cca_generate_exam_html.py --per-module 40`

> Note: The final exam uses `mdInline()` (same markdown rendering as `md()`) and is a sequential exam — all questions shown, no per-attempt rotation.

---

### Explanation Format Standard

#### Source format (what you write in the `.md` bank file)

The `<details>` block must be a **single paragraph** — no newlines. The renderer splits it at display time.

```
**X)** Why the correct answer is optimal — one or two sentences. A is wrong because [specific rule violated]. B is wrong because [specific reason]. C is wrong because [specific reason]. (source: Anthropic docs page name)
```

**Critical requirements:**
- `**X)**` prefix: correct letter in pre-shuffle order — the parser strips this and uses it as the answer index
- `(source: page name)` suffix: stripped at parse time, shown as docs reference on the results screen
- **Every wrong option must be addressed** by sentence starting with the original letter: `. A is wrong because`, `. B is wrong because`, etc.
- Use `. X is wrong` (period-space-letter-space-is) — this exact pattern is what `buildVerboseExplanation` splits on to create per-option blocks
- Also splits on `. Option X` if you prefer that phrasing
- Letters must refer to **pre-shuffle positions** (A/B/C/D as written in the `.md`) — the renderer remaps to post-shuffle display letters via `origToNew`

#### What the renderer produces at display time

`buildVerboseExplanation` converts the single paragraph into visually separated blocks:

```
Why the correct answer is optimal — one or two sentences.
─────────────────────────────────────────────────────────
A is wrong because [specific rule violated].
─────────────────────────────────────────────────────────
B is wrong because [specific reason].
─────────────────────────────────────────────────────────
C is wrong because [specific reason].
```

Wrong-option blocks are sorted A→B→C→D, then letters are remapped to post-shuffle display positions.

#### What NOT to write

```
❌ Narrative prose without split triggers:
"The correct answer is B because MCP provides a standard protocol. MCP is a software protocol, not
a hardware standard, and speed is not the differentiator."
→ Renders as a single block — no per-option breakdown visible.

❌ Labeled heading format (not split by renderer):
"**Why A is wrong:** MCP is a software protocol..."
→ md() renders the bold text but buildVerboseExplanation does not split on this pattern.

✅ Correct — uses ". X is wrong" split triggers:
"**B)** MCP provides a universal interface that replaces custom one-off integrations. A is wrong
because MCP is a software protocol, not a hardware standard. C is wrong because the standards body
that created USB-C did not create MCP. D is wrong because transfer speed is not the protocol's
primary design goal. (source: MCP integration)"
```

#### Known debt: converted concept banks

The four full-rotation concept banks (`practice-tests/concept-banks/concept-*.md`) were converted from old HTML quizzes that had narrative single-paragraph explanations. **These do not use `. X is wrong` split triggers** and therefore render as single blocks in the UI.

These files need their explanations rewritten to follow the format above before they reach the same quality standard as the module banks:
- `concept-agentic-loops.md` (30Q)
- `concept-mcp.md` (30Q)
- `concept-tool-use.md` (31Q)
- `concept-hooks.md` (30Q)

---

### HTML Quiz UI Standards

These standards are implemented in all quizzes generated by `cca_generate_module_quiz.py`.

#### Explanation Card (shown after answering)

| Element | Standard |
|---------|----------|
| Left border | `var(--red)` when incorrect, `var(--green)` when correct |
| "Your answer: X." label | Red + bold when incorrect, green + bold when correct |
| "Correct answer: X" | Always shown in white + bold |
| Explanation body | Split into per-option blocks, separated by a subtle divider: `border-top: 1px solid rgba(255,255,255,0.07)` |
| Wrong-option segment order | Sorted A→B→C→D, remapped to post-shuffle letters |
| Letter remapping | Wrong-option letters refer to pre-shuffle positions in source — the renderer remaps them to post-shuffle positions via an `origToNew` mapping at render time |

#### Results Screen

| Element | Standard |
|---------|----------|
| Wrong answer rows | `border-left: 3px solid var(--red)` + `background: rgba(251,113,133,0.06)` |
| Correct answer rows | `border-left: 3px solid var(--green)` + `background: rgba(74,222,128,0.05)` |

#### Nav Dots

| State | Style |
|-------|-------|
| Unanswered | Neutral border |
| Active (current question) | Accent fill |
| Answered correctly | Green border + green text (`answered-correct`) |
| Answered wrongly | Red border + red text (`answered-wrong`) |

---

#### Finish-Reading Play (Generate HTML Quiz)
1. Confirm topic scope from daily plan (`./cca read --date YYYY-MM-DD`).
2. Generate/update quiz artifact (e.g., `quizzes/cca-hooks-quiz.html`) using this flow.
3. Open and sanity-check locally:
   - `open quizzes/cca-{name}-quiz.html`
4. Start timed quiz run.

### 6. Post-Completion Tasks
When domain is completed (2 perfect passes):
1. Mark in Obsidian daily note: `02-Lanes/CCA-Cert/Daily/YYYY-MM-DD.md`
2. Update `docs/agent-memory.md` with dated entry
3. Optionally expand to `03-Knowledge/CCA-Domains/domain-N.md` with decision rules + anti-patterns
4. Record pass checkpoint event:
   - `./cca record-pass --date YYYY-MM-DD --method html --topic <topic> --quiz-file quizzes/cca-<topic>-quiz.html --score 1000 --perfect-run-count 2`
