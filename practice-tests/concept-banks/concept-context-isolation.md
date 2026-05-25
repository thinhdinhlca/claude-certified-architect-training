# Context Isolation — Question Bank

## Question 1
A data-science skill runs a lengthy exploratory analysis and appends hundreds of lines of intermediate output to the conversation. Subsequent questions about unrelated code features keep getting contaminated by those analysis tokens. Which single frontmatter change best prevents this?

A) Add `context: fork` to the skill frontmatter so the analysis runs in an isolated subagent context
B) Add `disable-model-invocation: true` to stop Claude from running the skill automatically
C) Move the skill to `~/.claude/skills/` so it is scoped to the user instead of the project
D) Add `user-invocable: false` so only Claude can invoke the skill internally

<details>
<summary>Answer</summary>

**A)** `context: fork` runs the skill in a forked subagent context, keeping all its verbose intermediate output out of the main conversation context window and preventing contamination of subsequent turns. B is wrong because `disable-model-invocation: true` only controls who can invoke the skill, not where it runs — the output still pollutes main context when you invoke it manually. C is wrong because changing scope (`~/.claude/skills/`) affects who can use the skill across projects, not whether its output stays isolated from the main conversation. D is wrong because `user-invocable: false` means only Claude can invoke it automatically, which does not address where the output lands in the context window. (source: Claude Code skills and workflows)

</details>

---

## Question 2
Your team stores coding standards, naming conventions, and "never do X" rules that every session must know. Where should these live?

A) `.claude/skills/standards/SKILL.md` with no `disable-model-invocation` flag
B) A shared skill invoked at the start of every session with `/standards`
C) `.claude/rules/standards.md` with a glob `paths: "**/*"` to cover all files
D) `.claude/CLAUDE.md` committed to the repository

<details>
<summary>Answer</summary>

**D)** `CLAUDE.md` is loaded at the start of every session, making it the correct home for always-applicable project standards that every developer and every task must follow. A is wrong because skills load only when invoked or when Claude decides they are relevant — there is no guarantee they are in context during every session. B is wrong because requiring manual invocation of `/standards` at every session start is operationally fragile — it depends on human or model compliance rather than deterministic loading. C is wrong because `.claude/rules/` files with `paths: "**/*"` trigger when Claude reads matching files, not at every session start, so they are not guaranteed to be loaded before the first file interaction. (source: Claude Code memory)

</details>

---

## Question 3
A developer's personal `/commit` skill overlaps in name with the project's `.claude/skills/commit/SKILL.md`. Which skill wins when the developer types `/commit`?

A) Claude Code raises an ambiguity error and asks the user to choose
B) Both skills merge their instructions and Claude executes both
C) The project skill at `.claude/skills/commit/SKILL.md` takes precedence over the personal skill
D) The personal skill at `~/.claude/skills/commit/SKILL.md` takes precedence because enterprise overrides personal, and personal overrides project

<details>
<summary>Answer</summary>

**D)** When skills share the same name across levels, enterprise overrides personal, and personal overrides project — so the personal skill at `~/.claude/skills/` wins over the project skill at `.claude/skills/`. A is wrong because Claude Code resolves the conflict silently using the documented priority order and does not prompt the user to choose. B is wrong because Claude Code does not merge conflicting skills — it applies the higher-priority definition and discards the lower one. C is wrong because the documented precedence is personal > project (with enterprise being the highest of all), not the other way around. (source: Claude Code skills and workflows)

</details>

---

## Question 4
A skill for running database migrations should never trigger automatically — only when the developer explicitly types `/db-migrate`. Which frontmatter field enforces this?

A) `allowed-tools: Bash`
B) `disable-model-invocation: true`
C) `user-invocable: false`
D) `context: fork`

<details>
<summary>Answer</summary>

**B)** `disable-model-invocation: true` prevents Claude from automatically loading or triggering the skill, ensuring it only runs when the user explicitly invokes it with `/db-migrate`. A is wrong because `allowed-tools: Bash` grants pre-approved tool access when the skill is active but does nothing to restrict invocation control. C is wrong because `user-invocable: false` does the opposite — it hides the skill from the slash menu so users cannot invoke it, while Claude still can. D is wrong because `context: fork` controls where the skill runs (isolated subagent vs. main context), not who can trigger it. (source: Claude Code skills and workflows)

</details>

---

## Question 5
An architect wants TypeScript-specific linting rules to automatically apply whenever Claude edits `.ts` or `.tsx` files, but not during unrelated Markdown edits in the same project. What is the correct mechanism?

A) Add `paths` frontmatter to a personal skill at `~/.claude/skills/typescript/SKILL.md`
B) Create `.claude/CLAUDE.md` with a section header `## TypeScript Rules` and rely on Claude to apply it contextually
C) Create `.claude/rules/typescript.md` with `paths: "**/*.{ts,tsx}"` in YAML frontmatter
D) Create a skill with `context: fork` that runs TypeScript checks on demand

<details>
<summary>Answer</summary>

**C)** `.claude/rules/` files with `paths` YAML frontmatter glob patterns load conditionally only when Claude works with files matching those patterns, giving deterministic, path-triggered rule application without loading for unrelated file types. A is wrong because the `paths` frontmatter in a skill controls when Claude automatically loads the skill based on file context, but a personal skill also affects only that one developer, not the whole team. B is wrong because CLAUDE.md loads entirely every session — you cannot scope sections of it to specific file types; Claude must infer when to apply them, which is probabilistic rather than deterministic. D is wrong because a forked skill requires explicit invocation and does not auto-apply when specific file types are opened. (source: Claude Code memory)

</details>

---

## Question 6
A team lead wants to restrict a code-review skill so it can use `Read` and `Grep` without permission prompts, but cannot call `Write` or `Edit` at all during review. Which configuration achieves this?

A) Set `allowed-tools: Read Grep` to pre-approve those two tools; add deny rules in permission settings to block Write and Edit
B) Set `allowed-tools: Read Grep` in frontmatter — this both pre-approves those tools and blocks all others
C) Set `disable-model-invocation: true` and restrict the skill manually to read-only operations in instructions
D) Set `context: fork` with `tools: Read, Grep` in a matching subagent definition

<details>
<summary>Answer</summary>

**A)** `allowed-tools` grants permission for listed tools without prompting, but it does not restrict other tools — every tool remains callable via normal permission flow. To actually block `Write` and `Edit`, deny rules must be added in permission settings. B is wrong because `allowed-tools` is not an allowlist that blocks unlisted tools; it only pre-approves the listed ones — Write and Edit remain callable through normal permission prompts. C is wrong because `disable-model-invocation: true` only restricts who can invoke the skill and relying on prose instructions to enforce tool access is probabilistic, not deterministic. D is wrong because `context: fork` runs the skill in a subagent, but tool restriction on the subagent requires a separate subagent definition; frontmatter alone on the skill does not wire this up. (source: Claude Code skills and workflows)

</details>

---

## Question 7
A developer wants a personal variation of the team's `/pr-review` skill that follows their own checklist, without affecting teammates who clone the repo. What is the correct approach?

A) Create `~/.claude/skills/pr-review/SKILL.md` and rely on personal override priority to shadow the project version silently
B) Create `~/.claude/skills/my-pr-review/SKILL.md` with a different name to avoid collision with the project skill
C) Edit `.claude/skills/pr-review/SKILL.md` in the project and add a personal section guarded by a comment
D) Create `~/.claude/skills/pr-review/SKILL.md` — this will not work because project skills take precedence over personal skills

<details>
<summary>Answer</summary>

**B)** Using a different name (`my-pr-review`) in `~/.claude/skills/` avoids the name collision problem entirely and guarantees the personal skill is always available without interfering with the project skill. A is wrong because while personal override priority means the personal skill would shadow the project one, this creates a silent discrepancy for the developer where the team's shared skill becomes invisible — using a different name is the documented correct approach. C is wrong because editing the project skill changes it for all teammates via version control — it is not a personal customization. D is wrong because it contains a false premise: personal skills actually take precedence over project skills with the same name, not the other way around. (source: Claude Code skills and workflows)

</details>

---

## Question 8
An exploration skill gathers codebase information verbosely before generating a design proposal. After running the skill, the developer notices the next unrelated prompt is slower and the context window indicator is much fuller. What is the root cause and correct fix?

A) The skill is running in the main conversation context; add `context: fork` so exploration output stays in an isolated subagent context
B) The session model is too capable; switch to Haiku with the `model: haiku` frontmatter field
C) The skill file is too large; split it into smaller skills under 500 lines
D) The skill is triggering too often; add `disable-model-invocation: true` to limit invocations

<details>
<summary>Answer</summary>

**A)** Without `context: fork`, the skill's verbose exploration output enters and stays in the main conversation context window, consuming tokens for all subsequent turns. Adding `context: fork` runs the skill in a forked subagent that returns only a summary, leaving the main context clean. B is wrong because switching to Haiku affects speed and cost but does not change where the skill's output lands in the context window — it still pollutes main context. C is wrong because splitting the skill into smaller files reduces its loaded size but does not prevent the output it generates from polluting the main conversation context. D is wrong because `disable-model-invocation: true` prevents Claude from auto-invoking the skill but the same context pollution occurs whenever the user invokes it manually. (source: Claude Code skills and workflows)

</details>

---

## Question 9
Which statement correctly describes how `.claude/rules/` files differ from CLAUDE.md for context loading?

A) Rules files are always loaded at session start just like CLAUDE.md, but in a separate memory layer
B) Rules files without `paths` frontmatter load unconditionally at launch; rules files with `paths` frontmatter load only when Claude works with matching files
C) Rules files only load when a user explicitly invokes them with a slash command
D) Rules files replace CLAUDE.md and are loaded instead of it for large projects

<details>
<summary>Answer</summary>

**B)** Rules files without `paths` frontmatter are loaded unconditionally at launch with the same priority as `.claude/CLAUDE.md`, while rules files with `paths` frontmatter are conditional — they load only when Claude reads files matching the specified glob patterns. A is wrong because there is no "separate memory layer" — rules without `paths` load at session start just like CLAUDE.md, while path-scoped rules load on demand. C is wrong because rules files are never invoked via slash commands — that is how skills work, not rules. D is wrong because rules files supplement CLAUDE.md, not replace it — both load and are concatenated into context. (source: Claude Code memory)

</details>

---

## Question 10
A skill triggers with `context: fork`. What context does the forked subagent start with compared to the main conversation?

A) The forked subagent inherits the full main conversation history including all prior turns
B) The forked subagent starts with a fresh context containing only the subagent system prompt plus basic environment details, not the main conversation history
C) The forked subagent inherits permission settings only and generates its own system prompt from the skill description
D) The forked subagent inherits only the CLAUDE.md content but not the conversation history

<details>
<summary>Answer</summary>

**B)** Subagents receive only their system prompt plus basic environment details (like working directory) — they do not receive the full Claude Code system prompt or main conversation history, which is precisely what makes them effective for context isolation. A is wrong because inheriting the full main conversation history would defeat the purpose of `context: fork` — the subagent is specifically designed to run in isolation from accumulated context. C is wrong because permission settings are not the only inheritance — the subagent uses the skill frontmatter as its configuration, with the skill body as its system prompt, independent of the parent session. D is wrong because Explore and Plan subagents explicitly skip CLAUDE.md files; custom forked subagents receive only the skill's system prompt, not CLAUDE.md. (source: Claude Code skills and workflows)

</details>

---

## Question 11
A new engineer joins a project and does not receive the "always use `pnpm` not `npm`" rule that all existing developers follow. The senior dev checked and the rule is in their `~/.claude/CLAUDE.md`. What is wrong and how should it be fixed?

A) The new engineer's Claude Code version is outdated; update to get the rule
B) The rule is not written concisely enough; rewrite it to be under 200 characters for proper propagation
C) The user-level `~/.claude/CLAUDE.md` is only loaded for that developer's sessions — not shared via version control; move the rule to the project-level `.claude/CLAUDE.md`
D) User-level CLAUDE.md requires each developer to run `/init` to merge personal settings into their session

<details>
<summary>Answer</summary>

**C)** `~/.claude/CLAUDE.md` is the user-level personal file — it applies across all of that developer's projects but is not committed to version control and is never shared with teammates. Moving the rule to `.claude/CLAUDE.md` in the repository ensures all developers receive it via version control. A is wrong because CLAUDE.md loading behavior does not depend on Claude Code version — this is a configuration scope problem, not a versioning problem. B is wrong because instruction length does not affect whether a rule is shared across developers — the scope (user vs. project) is what determines sharing. D is wrong because `/init` generates or improves a project's CLAUDE.md — it does not merge personal `~/.claude/CLAUDE.md` into the project's instructions. (source: Claude Code memory)

</details>

---

## Question 12
A `/fix-issue` skill shows just `fix-issue` in the slash menu with no hint about what argument to provide. The developer wants the autocomplete to display `fix-issue [issue-number]`. Which frontmatter field achieves this?

A) `when_to_use: "Use with an issue number"`
B) `argument-hint: "[issue-number]"`
C) `arguments: [issue-number]`
D) `description: "Fix GitHub issue [issue-number]"`

<details>
<summary>Answer</summary>

**B)** `argument-hint` is the frontmatter field specifically for controlling the hint text shown during autocomplete, e.g., `argument-hint: "[issue-number]"` displays the hint alongside the skill name in the slash menu. A is wrong because `when_to_use` provides additional context for Claude's automatic invocation decisions and is appended to the description — it does not affect the autocomplete parameter hint display. C is wrong because `arguments` declares named positional argument mappings for `$name` substitution within the skill body — it does not control the autocomplete hint text in the menu. D is wrong because `description` controls when Claude decides to auto-invoke the skill and what appears in the skill listing — it does not produce the autocomplete parameter hint. (source: Claude Code skills and workflows)

</details>

---

## Question 13
A team wants different rules for React components (`src/components/**/*.tsx`) vs. API handlers (`src/api/**/*.ts`) in the same monorepo. Both rule sets are large enough that loading both always would waste context. What is the optimal configuration?

A) Create two skills, one per file type, each with `context: fork` to isolate them
B) Create a single `.claude/CLAUDE.md` with both sections and instruct Claude in prose which section applies to which files
C) Create two separate rule files in `.claude/rules/` — one with `paths: "src/components/**/*.tsx"` and one with `paths: "src/api/**/*.ts"` — each in its own markdown file
D) Create `src/components/.claude/CLAUDE.md` and `src/api/.claude/CLAUDE.md` as subdirectory-level instructions

<details>
<summary>Answer</summary>

**C)** Path-scoped rule files in `.claude/rules/` with `paths` frontmatter are the designed mechanism for applying different rules to different file types — they load conditionally and deterministically based on which files Claude is working with. A is wrong because skills require explicit invocation or Claude auto-detection based on relevance — they are not automatically applied when specific file types are opened, and `context: fork` isolates output, not file-path triggering. B is wrong because CLAUDE.md loads its entire content every session with no ability to scope sections to specific file paths; Claude must infer applicability, which is unreliable. D is wrong because subdirectory CLAUDE.md files load on demand when Claude reads files in those directories, not based on file extension, and cannot distinguish `.tsx` from `.ts` within the same directory tree. (source: Claude Code memory)

</details>

---

## Question 14
An Explore subagent is used for Phase 1 of a large refactoring task. Which built-in characteristic makes it specifically useful for context isolation?

A) Explore pre-loads all project CLAUDE.md files to understand context before searching
B) Explore automatically compacts results using `/compact` before returning them
C) Explore runs with read-only tools and keeps its verbose search output in its own context, returning only a summary to the main conversation
D) Explore uses a more powerful model than the main conversation by default

<details>
<summary>Answer</summary>

**C)** The Explore subagent is optimized specifically as a read-only research agent: it has write tools denied, runs in its own context window, and returns only results to the main conversation — keeping verbose file search output, grep results, and logs out of main context. A is wrong because Explore and Plan subagents explicitly skip CLAUDE.md files to keep research fast and inexpensive, unlike other subagents. B is wrong because Explore does not automatically call `/compact` — it simply returns the summary from its isolated context without that mechanism. D is wrong because Explore uses Haiku by default, which is a faster and cheaper model than Sonnet — not a more powerful one; the speed choice prioritizes low latency. (source: Claude Code memory)

</details>

---

## Question 15
A skill at `.claude/skills/deploy/SKILL.md` has `allowed-tools: Bash(git add *) Bash(git commit *)`. What exactly does this accomplish?

A) It pre-approves these specific Bash patterns so Claude can run them without per-use permission prompts while the skill is active; other tools remain callable through normal permission flow
B) It permanently grants these Bash permissions to all sessions after the skill is first accepted
C) It restricts the skill to only these two Bash patterns — any other Bash command will be blocked when the skill is active
D) It grants permission only if the user has already trusted the project workspace; otherwise the field is ignored entirely

<details>
<summary>Answer</summary>

**A)** `allowed-tools` pre-approves the listed tools so Claude can use them without prompting during the skill's active scope; it does not restrict other tools — all other tools remain callable via normal permission prompts. B is wrong because the pre-approval is scoped to while the skill is active, not permanently granted to the entire session or future sessions. C is wrong because `allowed-tools` is a permission pre-approval list, not an allowlist that blocks unlisted tools — the skill can still use other tools subject to normal permission flow. D is wrong because the workspace trust requirement applies to whether the permission granted by `allowed-tools` takes effect at all — but once the workspace is trusted, the field applies as described, not just when manually accepted each time. (source: Claude Code skills and workflows)

</details>

---

## Question 16
A developer has a verbose `/analyze-dependencies` skill that floods context. They want to run it in isolation but also want the Explore subagent's read-only tool set for the job. Which frontmatter combination achieves both goals?

A) `disable-model-invocation: true` plus `allowed-tools: Read Grep Glob` — prevents auto-run and limits tools inline
B) `context: fork` alone — the forked subagent inherits read-only tools automatically when analyzing code
C) Move the skill to `~/.claude/skills/` and add `context: fork` — personal scope ensures isolation
D) `context: fork` plus `agent: explore` to explicitly use the Explore subagent's read-only tool configuration

<details>
<summary>Answer</summary>

**D)** `context: fork` runs the skill in an isolated subagent context, and `agent: explore` specifies that the Explore subagent type should be used — giving it the read-only tool set (Read, Grep, Glob) and Haiku model that Explore provides. A is wrong because `allowed-tools` pre-approves tools but does not isolate the skill's output from the main context — the verbose output still accumulates in the main conversation. B is wrong because `context: fork` alone uses a general-purpose subagent with full tool inheritance, not read-only tools — you need `agent: explore` to get the Explore configuration. C is wrong because personal scope (`~/.claude/skills/`) and `context: fork` together isolate context, but do not wire up the Explore read-only tool set — `agent: explore` is required for that. (source: Claude Code skills and workflows)

</details>

---

## Question 17
A project CLAUDE.md has grown to 350 lines covering testing conventions, API design, deployment procedures, and code style. Which refactoring best reduces always-loaded context while preserving correct behavior?

A) Delete CLAUDE.md and replace with a single large skill that covers everything, invoked automatically
B) Split into multiple imported files with `@path/to/file` syntax — all imported files still load at session start but organization improves
C) Move testing conventions and API design rules to `.claude/rules/` with appropriate `paths` patterns; keep permanent standards in CLAUDE.md; move deployment procedures to a skill
D) Use `claudeMdExcludes` to prevent the long CLAUDE.md from loading and rely on skills for all guidance

<details>
<summary>Answer</summary>

**C)** The optimal split is: always-applicable standards stay in CLAUDE.md, file-type-specific rules move to path-scoped `.claude/rules/` files (load only for matching files), and task-specific procedures like deployment move to skills (load only on invocation) — together minimizing always-loaded context. A is wrong because a skill that auto-invokes covers everything replaces the deterministic always-loaded behavior of CLAUDE.md with probabilistic auto-detection — universal standards may not load when Claude deems the skill irrelevant. B is wrong because `@import` syntax in CLAUDE.md expands all referenced files into context at launch — it improves organization but does not reduce tokens loaded per session. D is wrong because `claudeMdExcludes` is for excluding other teams' CLAUDE.md files in monorepos — using it on your own project's CLAUDE.md would eliminate all always-loaded context, requiring every standard to be re-discovered per task. (source: Claude Code memory)

</details>

---

## Question 18
A `/security-audit` skill inadvertently runs during routine code-completion tasks because Claude decides the description matches. Which frontmatter setting specifically prevents Claude from auto-loading it while keeping it available for explicit `/security-audit` invocations?

A) `context: fork`
B) `disable-model-invocation: true`
C) `paths: "src/security/**/*"`
D) `user-invocable: false`

<details>
<summary>Answer</summary>

**B)** `disable-model-invocation: true` prevents Claude from automatically loading the skill based on description matching, while the user can still explicitly type `/security-audit` to run it. A is wrong because `context: fork` isolates the skill's output but does not prevent Claude from auto-loading it — it would still trigger during routine tasks. C is wrong because `paths` limits when Claude auto-loads the skill to matching file paths, but this would just change when Claude auto-loads it, not prevent automatic loading entirely. D is wrong because `user-invocable: false` does the opposite of what is needed — it hides the skill from the slash menu so users cannot invoke it directly, while Claude can still invoke it automatically. (source: Claude Code skills and workflows)

</details>

---

## Question 19
Which statement about the Explore subagent and CLAUDE.md loading is accurate?

A) Explore skips CLAUDE.md files and git status to keep research fast and inexpensive
B) Explore loads only the user-level `~/.claude/CLAUDE.md` but not project-level CLAUDE.md
C) Explore loads all CLAUDE.md files to understand project context before searching
D) Explore loads CLAUDE.md files only when the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` env var is set

<details>
<summary>Answer</summary>

**A)** Explore (and Plan) are specifically documented to skip CLAUDE.md files and the parent session's git status to keep research fast and cost-efficient — unlike other built-in and custom subagents which load both. B is wrong because Explore skips all CLAUDE.md files regardless of scope — not just project-level. C is wrong because loading CLAUDE.md would add latency and tokens to what is designed to be a fast, cheap research operation — the docs explicitly state Explore skips it. D is wrong because `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` controls loading CLAUDE.md from `--add-dir` directories for the main session, not for Explore subagents. (source: Claude Code memory)

</details>

---

## Question 20
A team uses a `/generate-api-endpoint` skill that includes exemplar endpoint code for consistency. The skill is loaded on every session start, consuming significant context even during debugging tasks. What is the simplest fix?

A) Add `context: fork` to isolate the heavy exemplar content in a subagent
B) Move the exemplar code to `.claude/rules/` with a `paths: "src/api/**/*.ts"` pattern
C) Keep it as a skill with its default configuration — skills only load their body when invoked, not at session start
D) Move the exemplar code to CLAUDE.md with a comment marking it as optional

<details>
<summary>Answer</summary>

**C)** Skills load only their description into context at session start; the full skill body loads only when invoked. If the skill body is consuming significant context every session, the more likely cause is it is in CLAUDE.md rather than properly in a skill — a correctly configured skill already has on-demand body loading built in. A is wrong because `context: fork` affects where the skill runs, not when its body loads — the context problem during startup is about the description vs. body distinction, not execution isolation. B is wrong because moving exemplar code to a path-scoped rule would load it whenever `src/api/**/*.ts` files are touched, including during debugging those API files — not just endpoint generation. D is wrong because CLAUDE.md is always fully loaded; adding exemplar code there and marking it "optional" does not prevent it from consuming tokens every session. (source: Claude Code skills and workflows)

</details>

---

## Question 21
A developer writes a personal preference skill for code style at `~/.claude/skills/style/SKILL.md`. The project also has `.claude/skills/style/SKILL.md` with team conventions. Which skill runs when the developer types `/style`?

A) Claude Code raises a conflict warning and disables both until the developer resolves the collision
B) Claude merges both skill bodies and presents a combined set of instructions
C) The personal skill at `~/.claude/skills/style/SKILL.md` wins because personal scope takes precedence over project scope
D) The project skill at `.claude/skills/style/SKILL.md` wins because project settings override personal settings

<details>
<summary>Answer</summary>

**C)** The documented skill precedence is: enterprise > personal > project. Therefore the personal skill at `~/.claude/skills/` takes precedence over the project skill at `.claude/skills/`. A is wrong because Claude Code silently resolves name conflicts using the documented priority order rather than raising warnings or disabling skills. B is wrong because Claude Code does not merge conflicting skills from different scopes — it applies the higher-priority definition only. D is wrong because the precedence order is personal over project, not project over personal — project skills have lower priority than personal skills. (source: Claude Code skills and workflows)

</details>

---

## Question 22
A scenario presents three problems simultaneously: (1) the skill output floods the main conversation with 200 lines of logs, (2) the skill can currently run `rm -rf` during cleanup, and (3) there is no hint in the slash menu showing expected arguments. Which frontmatter combination resolves all three?

A) `context: fork` + `user-invocable: false` + `argument-hint: "[target-path]"`
B) `context: fork` + `allowed-tools: Bash(git *) Bash(ls *)` + `argument-hint: "[target-path]"`
C) `disable-model-invocation: true` + `allowed-tools: Bash(git *)` + `argument-hint: "[target-path]"`
D) `context: fork` + `allowed-tools: Bash(rm -rf *)` + `description: "Use with [path]"`

<details>
<summary>Answer</summary>

**B)** `context: fork` isolates verbose output (problem 1); adding deny rules in permission settings for `rm -rf` combined with `allowed-tools` pre-approving safe patterns addresses the tool concern (problem 2); `argument-hint: "[target-path]"` provides the autocomplete hint (problem 3). A is wrong because `user-invocable: false` hides the skill from the slash menu entirely, preventing manual invocation — it does not solve problem 3, it eliminates the invocation path. C is wrong because `disable-model-invocation: true` prevents auto-loading but does not isolate verbose output from the main context window when manually invoked — it does not solve problem 1. D is wrong because `allowed-tools: Bash(rm -rf *)` would pre-approve the dangerous destructive command rather than restricting it — this makes problem 2 worse. (source: Claude Code skills and workflows)

</details>

---

## Question 23
A monorepo has packages with their own `.claude/skills/` directories under `packages/frontend/.claude/skills/` and `packages/backend/.claude/skills/`. How does Claude Code discover these nested skills?

A) They load at session start because Claude Code recursively scans all `.claude/skills/` directories in the project tree
B) They are never discovered; only the root `.claude/skills/` is scanned
C) They require explicit `--add-dir` flags pointing to each package directory
D) Claude Code discovers nested package skills on demand when Claude works with files in those subdirectories

<details>
<summary>Answer</summary>

**D)** Claude Code discovers skills from nested `.claude/skills/` directories on demand when Claude reads files in those subdirectories — for example, editing `packages/frontend/` triggers discovery of `packages/frontend/.claude/skills/`. A is wrong because nested subdirectory skills load on demand (not at session start) — only root-level `.claude/skills/` and parent-directory skills load at launch. B is wrong because nested package skills are explicitly supported for monorepo setups — the docs describe this pattern as a feature, not a limitation. C is wrong because `--add-dir` grants file access to external directories; discovering nested skills within the existing project tree happens automatically without `--add-dir`. (source: Claude Code skills and workflows)

</details>

---

## Question 24
A developer wants background knowledge about a legacy authentication system in a skill — Claude should use this knowledge when relevant, but `/legacy-auth` should not appear as an invokable command in the slash menu. Which frontmatter field accomplishes this?

A) `argument-hint: ""` to show an empty hint
B) `disable-model-invocation: true`
C) `context: fork`
D) `user-invocable: false`

<details>
<summary>Answer</summary>

**D)** `user-invocable: false` hides the skill from the slash menu so users cannot invoke it directly, while Claude can still load it automatically when relevant — perfect for background knowledge skills. A is wrong because `argument-hint` is only for controlling the hint text shown during autocomplete, not for hiding the skill from the menu entirely. B is wrong because `disable-model-invocation: true` does the opposite: it prevents Claude from auto-loading the skill and lets only the user invoke it via the slash menu. C is wrong because `context: fork` controls execution isolation, not invocation visibility — the skill would still appear in the slash menu with `context: fork` alone. (source: Claude Code skills and workflows)

</details>

---

## Question 25
A team needs deployment procedures documented in Claude's memory. Deployments involve multi-step side-effect-heavy workflows that must never run accidentally. Universal code standards must always be in context. Path-specific API rules are needed only for API files. Which mapping is correct?

A) Deployment → CLAUDE.md, Standards → skill, API rules → `.claude/rules/` with paths
B) Deployment → `.claude/rules/` with `paths: "deploy/**"`, Standards → CLAUDE.md, API rules → skill
C) Deployment → CLAUDE.md section, Standards → `.claude/rules/`, API rules → skill with `context: fork`
D) Deployment → skill with `disable-model-invocation: true`, Standards → CLAUDE.md, API rules → `.claude/rules/` with paths

<details>
<summary>Answer</summary>

**D)** Deployment procedures with side effects → skill with `disable-model-invocation: true` (manual control, on-demand only); universal code standards → CLAUDE.md (always loaded); path-specific API rules → `.claude/rules/` with `paths` (conditional loading by file path). A is wrong because putting deployment in CLAUDE.md makes it always loaded, which wastes context on every session, and using a skill for standards means they may not always be in context. B is wrong because a `.claude/rules/` file with `paths: "deploy/**"` would load deployment instructions whenever deploy-path files are touched, not just when deploying — and a forked skill for API rules requires explicit invocation instead of automatic path-based triggering. C is wrong because CLAUDE.md sections cannot be scoped by file path, and path-scoped rules are the correct mechanism for API rules rather than skills. (source: Claude Code memory)

</details>

---

## Question 26
After running a `context: fork` skill, the developer asks a follow-up question about the skill's output in the main conversation. How does Claude access that output?

A) Claude cannot access the output at all — forked context is fully isolated with no return path
B) The forked context is merged back into the main context window when the skill completes
C) The skill returns a summary or result to the main conversation, which Claude can reference in follow-ups
D) Claude re-reads the skill's output from the forked subagent's context directly

<details>
<summary>Answer</summary>

**C)** A forked subagent works independently and returns its results to the main conversation — the summary or output becomes visible in the main context while the verbose intermediate work stays isolated in the subagent context. A is wrong because forked subagents do return results to the main conversation; the isolation prevents verbose intermediate output from contaminating context, not the final result. B is wrong because the forked context is not merged back — only the returned summary appears in the main context, not the full subagent conversation history. D is wrong because Claude in the main conversation cannot directly read the forked subagent's internal context — it only sees what the subagent returns. (source: Claude Code skills and workflows)

</details>

---

## Question 27
A developer creates an `argument-hint` like `"[branch] [environment]"` in their deployment skill frontmatter. What does this directly control?

A) The hint text displayed during slash command autocomplete to indicate expected arguments
B) Named variable substitution — `$branch` and `$environment` become available in the skill body
C) The order in which `$ARGUMENTS[0]` and `$ARGUMENTS[1]` are bound in the skill body
D) Validation logic that rejects invocations with fewer than two arguments

<details>
<summary>Answer</summary>

**A)** `argument-hint` controls only the hint text shown during autocomplete in the slash menu — it is a UI affordance showing what arguments to provide, not a functional argument binding or validation mechanism. B is wrong because named variable substitution requires the `arguments` frontmatter field (e.g., `arguments: [branch, environment]`), not `argument-hint` — the hint field has no effect on `$name` expansion. C is wrong because `$ARGUMENTS[0]` and `$ARGUMENTS[1]` binding is determined by the positional arguments the user types, not by anything in `argument-hint`. D is wrong because `argument-hint` provides no validation logic — Claude Code does not enforce argument count based on the hint; it is purely informational display text. (source: Claude Code skills and workflows)

</details>

---

## Question 28
A project has two files: `.claude/CLAUDE.md` (team-shared instructions) and `CLAUDE.local.md` (personal per-project preferences, gitignored). When both exist, in what order does Claude see them?

A) They are interleaved alphabetically during context loading
B) `.claude/CLAUDE.md` is loaded first; then `CLAUDE.local.md` is appended after at the same directory level — personal notes appear last within that level
C) `CLAUDE.local.md` is loaded first; `.claude/CLAUDE.md` is loaded second
D) `.claude/CLAUDE.md` is appended after `CLAUDE.local.md` in load order — personal notes win by appearing last

<details>
<summary>Answer</summary>

**B)** Within each directory level, `CLAUDE.local.md` is appended after `CLAUDE.md` — so `.claude/CLAUDE.md` loads first, then `CLAUDE.local.md` appends after it, making personal notes the last thing Claude reads at that level. A is wrong because there is no alphabetical interleaving — the load order follows a documented rule: CLAUDE.md first, CLAUDE.local.md second at each directory level. C is wrong because `CLAUDE.local.md` is not loaded before the project CLAUDE.md; the order within a directory level is CLAUDE.md first, then CLAUDE.local.md. D is wrong in framing — the load order described in option B is correct; CLAUDE.local.md does appear last, but this option misdescribes the mechanism as CLAUDE.md being "appended after". (source: Claude Code memory)

</details>

---

## Question 29
A skill invokes successfully and its content enters the conversation. After many more turns and auto-compaction, the skill seems to stop influencing Claude's behavior. What is the most likely cause and correct response?

A) `allowed-tools` grants expired after compaction — re-trust the workspace to restore permissions
B) The model switched to Haiku during compaction and doesn't load skill content — switch back with `/model`
C) The skill file on disk was edited and the in-memory copy expired — restart Claude Code
D) The skill content may have been dropped during compaction; re-invoke the skill to restore its full content

<details>
<summary>Answer</summary>

**D)** Auto-compaction summarizes conversation history within a token budget and re-attaches the most recently invoked skills up to a combined 25,000-token cap, keeping the first 5,000 tokens of each. Older or larger skills can be dropped entirely — re-invoking the skill restores its full content. A is wrong because `allowed-tools` grants are tied to the skill's active scope during a turn, not to a session-level cache that compaction could invalidate. B is wrong because the model does not automatically switch during compaction — the session model remains consistent unless you explicitly change it. C is wrong because Claude Code does not have an "in-memory cache expiry" for skills — the skill file on disk is not re-read mid-session unless you explicitly re-invoke. (source: Claude Code skills and workflows)

</details>

---

## Question 30
A team lead wants to ensure security-review instructions are never visible to Claude in sessions unrelated to security work, while still being instantly available when `/security-review` is typed. Which combination of frontmatter fields achieves this?

A) `disable-model-invocation: true` + `context: fork` — description stays out of context, body loads only on explicit invocation in isolated subagent
B) `paths: "src/security/**/*"` + `disable-model-invocation: true` — loads only for security files
C) `user-invocable: false` + `context: fork` — hides from menu and isolates output
D) `disable-model-invocation: true` alone — keeps description out of context and body out until invoked

<details>
<summary>Answer</summary>

**A)** `disable-model-invocation: true` removes the skill's description from the always-loaded skill listing (so Claude does not see it during unrelated sessions) and ensures only the user can invoke it; `context: fork` then runs the security review in isolation when explicitly called. B is wrong because `paths: "src/security/**/*"` would load the skill whenever Claude works with security files, which is still visible during security-file editing tasks outside a deliberate security review invocation. C is wrong because `user-invocable: false` hides the skill from the slash menu, which is the opposite of what is needed — the team lead wants `/security-review` to be explicitly invokable. D is wrong because `disable-model-invocation: true` alone does achieve the "not visible to Claude" goal, but the team lead also wants the security review to run in its own isolated context — `context: fork` adds that. (source: Claude Code skills and workflows)

</details>

---
