# CCA Exam — What I Learned From My First Pass

## What the exam actually tests

It's not a trivia test. Every question is: "Here's a system with a real problem. What do you do?" You're making decisions under constraints, not recalling definitions.

The wrong answers are designed to catch you if you half-know the material — they're technically plausible, similar length, no obvious gimmicks. The right answer is usually the one that respects a specific constraint stated in the question. Read carefully.

## The biggest shift in how I prepared

I stopped reading documentation passively and started building a mental model of **how Claude-based systems work end-to-end**. What happens when a tool fails? What context does a subagent actually have? What does the coordinator see that the subagent doesn't? The exam rewards understanding the system's behavior, not memorizing its parts.

## What each scenario really tests

| Scenario | It's not about... | It's about... |
|----------|-------------------|---------------|
| Code Generation w/ Claude Code | Knowing every config file | Understanding which config mechanism solves which problem — `context: fork` for isolation, skills for on-demand, CLAUDE.md for always-applied, `.claude/rules/` for path-specific |
| Multi-Agent Research | Agent names and roles | How information and errors flow between agents. What gets passed explicitly vs what's assumed. Where recovery should happen — locally or at coordinator level |
| CI/CD with Claude Code | Command memorization | When to optimize for cost (batch) vs latency (sync). How to structure reviews to avoid confirmation bias. How to make automated feedback trustworthy |
| Customer Support Agent | Tool API details | When to enforce behavior programmatically vs when prompt guidance is enough. How to decide: escalate now or resolve first? |

## The patterns that repeat across every scenario

Six patterns showed up in nearly every question:

**1. Context isolation** — "This thing is polluting that thing's context." Answer is usually: fork, subagent delegation, or conditional loading. Not "add more instructions."

**2. Error handling** — "Something failed. Now what?" The answer involves structure (what failed + what was attempted + what partial results exist), not silence or generic messages.

**3. Tool selection** — "The agent keeps picking the wrong tool." Start with the tool description. Fix the root cause before adding routing layers or preprocessors.

**4. Batch vs sync** — "Should I use batch for this?" If someone's waiting on the result, no. If it runs overnight and nobody cares about latency, yes.

**5. Few-shot decision boundary** — This one got me. Few-shot is often right, but not when the problem varies unpredictably across cases. Then the answer is self-evaluation or structural change. Don't default to few-shot reflexively.

**6. Config scope** — "Should this live in the project or the user's home directory?" Project = shared via git, everyone gets it. User = personal, not shared. Skills in the same name: project wins.

## What I'd tell myself before taking it again

Focus your study on **understanding why things fail and how Claude recovers**. Read the docs, but then build a mental simulation of what happens at each step. Most questions boil down to: something went wrong, or something could go wrong, and you need to pick the right guardrail — not the most complex one, not the one that sounds smartest, but the one that matches the actual constraint in the scenario.

And slow down. You have time.
