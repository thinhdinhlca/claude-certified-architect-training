# CCA Tool Use Quiz — Handoff for Codex

**File:** `quizzes/cca-tool-use-quiz.html`  
**Purpose:** Self-contained HTML quiz for CCA Domain 1 (Tool Use & Agent Architecture)  
**Last updated:** 2026-05-10  
**See also:** `docs/quiz-generation/QUIZ-GENERATION-FLOW.md` for the standardized quiz creation process

## Rules the User Established

1. **30-question bank** in the file. Each attempt randomly picks **20** with shuffled answer orders.
2. **Pass = 100%** (all 20 correct, 1000/1000). No partial passes.
3. **2 perfect passes required** to mark the domain complete.
4. Questions AND answer positions must be shuffled every attempt.
5. Must be a self-contained HTML file (no build step, no framework).

## Architecture

Single HTML file, vanilla JS, no dependencies. Three screens managed by a state machine:

```
start → quiz → results → (retry) → quiz → ...
```

### State (`var S`)
```
{
  screen: 'start' | 'quiz' | 'results',
  pool: [],          // 20 selected, option-shuffled questions
  ix: 0,             // current question index
  answers: {},       // {questionIndex: selectedOptIndex}
  revealed: false,
  timeLeft: 90 * 60, // seconds (90 min)
  timerId: null,
  score: null,
  review: [],        // [{q, selected, isCorrect}]
  passCount: 0       // perfect runs in this browser session
}
```

### Question shape in BANK
```js
{
  source: "Tool Definitions",           // topic label shown on card
  prompt: "The question text...",       // HTML allowed (<strong>, <code>)
  opts: ["A text", "B text", ...],      // 4 options
  ans: 1,                               // index of correct answer (0-based)
  expl: "Explanation text..."           // HTML allowed, shown on reveal
}
```

### Key functions
| Function | Role |
|----------|------|
| `buildDeck()` | Shuffles BANK, takes first 20, shuffles opts within each |
| `shuffleOpts(q)` | Randomizes option order, returns {opts, correctIdx} |
| `startQuiz()` | Builds deck, resets state, starts 90-min timer |
| `finishQuiz()` | Scores, increments passCount if perfect, records wrong answers, shows results |
| `renderQuiz()` | Renders question card with option list + nav dots |
| `renderResults()` | Score, pass tracker, topic breakdown, weak areas, review list |
| `loadWrongs()` / `saveWrongs()` | Read/write wrong answers from localStorage |
| `clearWrongs()` | Remove wrong answers from localStorage |

### Event handling
All via delegated click listener on `#app` — checks `e.target.id` or `e.target.closest()` for `.option`, `.qnav-dot`.

## Pass Tracking

- `S.passCount` increments only on perfect scores (1000/1000).
- Reset to 0 only via "Reset Progress" button or page reload.
- Persistence: `localStorage.setItem('cca_domain1_pass_count', S.passCount)` in `finishQuiz()` and read on init.
- Wrong answers: `localStorage.setItem('cca_domain1_wrong_answers', JSON.stringify([...]))` accumulates misses across sessions.
- Clear wrongs: `localStorage.removeItem('cca_domain1_wrong_answers')` via "Clear Weak Areas" button.

### Wrong Answer Storage Shape
```js
// localStorage key: cca_domain1_wrong_answers
[
  {
    source: "Extended Thinking",      // topic label
    prompt: "You set thinking: ...",  // question text
    selected: 0,                      // what user picked (shuffled index)
    correct: 1,                       // correct answer (shuffled index)
    timestamp: 1746825600000          // Date.now()
  }
]
```

## CSS

Dark theme. CSS variables in `:root` for easy color swaps. Key classes:
- `.option.selected` / `.correct` / `.wrong` for answer states
- `.pass-dot.earned` for tracker circles
- `.pass-square.cleared` for results pass squares
- `.timer.warning` / `.danger` for time alerts

## Known Issues / Improvement Areas

1. **No localStorage persistence** — passCount resets on page reload. Add save/load.
2. **Timer doesn't warn before auto-submit** — only visual color change. Add 5-min warning dialog.
3. **No "mark for review"** — user can't flag questions to revisit.
4. **Category breakdown + Weak Areas** — results show per-topic breakdown AND accumulated weak areas from localStorage. ✅ Implemented.
5. **No CSV/export** — results can't be saved for the daily log.
6. **No keyboard shortcuts** — only mouse clicks. Add 1/2/3/4 or A/B/C/D keys.
7. **No dark/light toggle** — single theme only.
8. **Explanations could link to Obsidian notes** — add `obsidian://open?vault=CCA-Study&file=...` links.
9. **Shuffle-proof explanations** — all 30 explanations rewritten to remove letter references. ✅ Implemented.
10. **Wrong answer tracking** — misses stored in localStorage (`cca_domain1_wrong_answers`), accumulated across sessions, grouped by topic in results. ✅ Implemented.

## How to Add Questions

1. Add objects to `BANK` array with `source`, `prompt`, `opts` (4 strings), `ans` (0-3 index of correct), `expl`.
2. Update the count on the start screen text if changing from 30.
3. All options are shuffled per-attempt automatically.
4. Sources should match existing ones for consistency: `"Tool Definitions"`, `"Tool Descriptions"`, `"Tool Consolidation"`, `"Tool Namespacing"`, `"Input Examples"`, `"Model Selection"`, `"Tool Choice"`, `"Extended Thinking"`, `"Adaptive Thinking"`, `"Interleaved Thinking"`, `"Thinking Display"`, `"Effort Parameter"`, `"Tool Use System Prompt"`, `"Tool Responses"`, `"Tool Design"`.

## Testing It

```bash
open quizzes/cca-tool-use-quiz.html
```

No server needed — works from `file://` protocol. All JS is IIFE-wrapped, no globals leak.

## Source Material

All questions drawn from:
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- https://platform.claude.com/docs/en/build-with-claude/extended-thinking
- https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking
- https://www.anthropic.com/engineering/writing-tools-for-agents
