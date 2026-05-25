# Module Bank: Code Generation with Claude Code

Auto-generated bank with 30 questions.

## Question 1
You're building a Python data pipeline service. The repo root has a CLAUDE.md with general Python style rules. You also have a `.claude/` directory with a `CLAUDE.md` that adds data-pipeline-specific conventions (e.g., always use `pandas` over raw loops for tabular ops). A developer reports that Claude is ignoring the pipeline conventions when generating new ETL modules. What is the most likely cause?

A) `.claude/CLAUDE.md` overrides the repo-root `CLAUDE.md` entirely, so the general rules are silently dropped along with the pipeline rules.
B) Only the repo-root `CLAUDE.md` is loaded automatically; `.claude/CLAUDE.md` requires an explicit `@.claude/CLAUDE.md` import in the root file to be included.
C) The `.claude/CLAUDE.md` conflicts with the root `CLAUDE.md` on style topics, and Claude silently picks the root when conflict is detected.
D) `.claude/` is reserved for settings and skills; `CLAUDE.md` placed there is never loaded by Claude Code.

<details><summary>Answer</summary>
**B)** `.claude/CLAUDE.md` is not auto-loaded; only the repo-root `CLAUDE.md` is. To include it, the root file must contain `@.claude/CLAUDE.md` as an import directive. A is wrong because `.claude/CLAUDE.md` does not override the root — it is simply not loaded unless imported. C is wrong because there is no conflict-detection mechanism that silently resolves rule collisions. D is wrong because `.claude/CLAUDE.md` can be used for context but requires explicit import via the `@` directive to take effect. (source: CLAUDE.md guide)
</details>

## Question 2
Your Go microservices repo has three services in `services/auth/`, `services/billing/`, and `services/notifications/`. Each service has subtly different error-handling patterns and logging conventions. You want Claude to automatically apply the correct conventions depending on which service directory is active. What is the right approach?

A) Add a root CLAUDE.md section per service with prose headers like "## Auth service conventions" and rely on Claude to select the right section.
B) Place a separate CLAUDE.md inside each `services/<name>/` directory so conventions auto-load when files in that subtree are opened or edited.
C) Create one skill per service (e.g., `/auth-context`, `/billing-context`) that developers must invoke before working on each service.
D) Use `.claude/rules/` files with `globs: ["services/auth/**"]` frontmatter so each rule file activates only for its matching service path.

<details><summary>Answer</summary>
**D)** `.claude/rules/` files with glob-based frontmatter are the designed mechanism for path-conditional rule activation. Each rules file loads deterministically when a matched file is in scope. B is wrong because per-directory CLAUDE.md files work but require developers to `cd` into each service directory; glob-based rules are more reliable across IDEs and multi-file operations. A is wrong because prose headers with conditional intent are non-deterministic. C is wrong because skill invocation is manual and creates workflow friction — rules activate automatically. (source: Claude Code settings)
</details>

## Question 3
You are generating Terraform modules for a new AWS VPC. The task is well-understood and low-risk: create a standard three-tier network with public/private/data subnets. Claude is configured with auto-approve on file writes. Which execution approach is most appropriate here?

A) Use plan mode to review the full Terraform structure before any files are written, then approve manually.
B) Force manual approval on every tool call so you can inspect each `resource` block as it is written.
C) Direct execution with auto-approve is appropriate — the scope is clear, the task is well-understood, and the risk of file writes is low.
D) Run Claude in a forked sub-agent so the main session context is not contaminated with Terraform boilerplate.

<details><summary>Answer</summary>
**C)** Direct execution with auto-approve is appropriate when scope is clear and well-defined, the risk is low, and the task is standard. Forcing plan mode or manual approval on routine, low-risk generation adds latency without meaningful safety benefit. A is wrong because plan mode is valuable for risky or uncertain operations, not for well-understood boilerplate generation. B is wrong because per-call manual approval would be disruptive and offers no benefit on a predictable task. D is wrong because context isolation via fork is meant to prevent cross-contamination, not to handle boilerplate output. (source: Plan mode documentation)
</details>

## Question 4
Your team maintains a React component library. You want Claude to automatically run `npm test -- --watchAll=false` after every batch of component edits and report failures without human intervention. What is the correct mechanism in Claude Code?

A) Add a post-tool hook in `.claude/settings.json` that triggers `npm test` after every `Edit` tool call.
B) Create a `/test-after-edit` skill that developers invoke manually after each edit session.
C) Add `autoTest: true` to `.claude/settings.json` — Claude Code will infer the test command from the nearest `package.json`.
D) Configure `always-run: npm test` in the project CLAUDE.md so Claude executes it before completing any response.

<details><summary>Answer</summary>
**A)** Post-tool hooks in `.claude/settings.json` fire after specified tool calls, making them the correct mechanism for automatic post-edit actions like running tests. B is wrong because skills require manual invocation and cannot run automatically. C is wrong because `autoTest` is not a valid `settings.json` field. D is wrong because `always-run` is not a CLAUDE.md directive; CLAUDE.md provides context and instructions, not executable triggers. (source: Claude Code settings)
</details>

## Question 5
You are refactoring a large Go codebase: renaming a core interface `DataStore` to `Repository` across 47 files. You are considering whether to do this as a single atomic operation or to break it into phases. What is the strongest argument for breaking it into phases with incremental commits?

A) Incremental commits let you run the test suite between phases, catch regressions early, and roll back individual phases if something goes wrong.
B) Atomic commits confuse the `git blame` history for interface renames; incremental commits keep blame clean.
C) Claude Code cannot hold more than ~20 files in context at once, so phased editing is mandatory for correctness.
D) Claude's edit accuracy degrades non-linearly above 10 simultaneous file edits, so phases are required for quality.

<details><summary>Answer</summary>
**A)** Incremental commits with test runs between phases is the correct rationale: it enables regression detection, provides rollback granularity, and keeps the codebase in a compilable state throughout. B is wrong because `git blame` clarity is a minor consideration, not the strongest safety argument. C is wrong because context limits don't impose a hard file-count cap of 20; subagents can handle broad exploration. D is wrong because there is no documented non-linear accuracy degradation at a specific file-edit threshold. (source: Claude Code best practices)
</details>

## Question 6
A data engineering team has a shared project with SQL generation workflows. The team's `.claude/settings.json` allowlist currently permits `Bash`, `Read`, and `Edit`. A new workflow needs to run `psql` queries against a local dev database. The team lead wants only senior engineers to be able to approve new Bash subcommands. What is the correct settings configuration?

A) Add `psql` to the denylist in `.claude/settings.json` so it is blocked by default, and seniors override it via `--allow` at runtime.
B) Remove `Bash` from the allowlist entirely so all shell commands require per-call approval; seniors approve `psql` invocations individually.
C) Add `Bash(psql:*)` to the allowlist in the project `.claude/settings.json` committed to the repo so all users with repo access can run psql.
D) Keep `Bash` on the allowlist but add `psql` to a `requireApproval` list so Claude prompts before executing any psql subcommand.

<details><summary>Answer</summary>
**C)** The tool allowlist in `.claude/settings.json` supports granular patterns like `Bash(psql:*)` to permit specific subcommands. Committing this to the repo gives all authorized team members the permission automatically. B is wrong because removing `Bash` entirely would break all existing shell commands. A is wrong because a denylist entry for `psql` would block it for everyone with no override mechanism at the tool level. D is wrong because `requireApproval` is not a valid field in `settings.json`'s tool permission model. (source: Claude Code settings)
</details>

## Question 7
You are generating an OpenAPI client in Python from a large spec file. The spec is 8,000 lines and you want Claude to read it completely before generating the client. You notice Claude is summarizing sections rather than reading the full spec. What CLAUDE.md instruction best addresses this?

A) Add `max_read_lines: unlimited` to CLAUDE.md so Claude is not artificially truncated when reading spec files.
B) Include an explicit instruction in CLAUDE.md: "When generating API clients, always read the complete source spec file before writing any code. Do not summarize or skip sections."
C) Add a `.claude/rules/` file with `globs: ["**/*.yaml"]` that instructs Claude to use a sub-agent with a large context window for YAML files.
D) Set `context_mode: full` in `.claude/settings.json` to disable Claude's auto-summarization heuristics.

<details><summary>Answer</summary>
**B)** Explicit behavioral instructions in CLAUDE.md are the correct way to override Claude's default summarization tendencies for specific task types. Clear prose directives ("always read the complete file") are effective context steering. A is wrong because `max_read_lines` is not a valid CLAUDE.md field. C is wrong because routing based on file extension via sub-agent does not prevent summarization — it only changes which agent does it. D is wrong because `context_mode` is not a valid `settings.json` field. (source: CLAUDE.md guide)
</details>

## Question 8
Two engineers are working in parallel on the same Claude Code project: one refactoring the React frontend and one migrating the PostgreSQL schema. They share a project-level CLAUDE.md with rules for both layers. Each engineer reports that Claude keeps mixing context from the other's work domain into suggestions. What is the correct fix?

A) Each engineer creates a personal `~/.claude/CLAUDE.md` with domain-specific instructions that override the shared project CLAUDE.md.
B) Each engineer runs their session in a separate worktree and invokes skills with `context: fork` so sub-agents are isolated per domain.
C) The project CLAUDE.md should be split into domain sections with conditional headers so Claude auto-selects the relevant section per engineer.
D) Use `.claude/rules/` with glob patterns scoped to `src/` for the frontend engineer and `migrations/` for the schema engineer so rules activate per working path.

<details><summary>Answer</summary>
**D)** Glob-scoped rules files are the cleanest solution: frontend rules activate for `src/**` files, migration rules activate for `migrations/**` files, and neither bleeds into the other. B is wrong because `context: fork` applies to skill sub-agents, not to separate engineer sessions — worktrees do help but the root cause is untargeted context, not session isolation. A is wrong because personal CLAUDE.md files add personal context; they don't suppress the project's cross-domain pollution. C is wrong because conditional prose headers are unreliable — Claude may still pull from irrelevant sections. (source: Claude Code settings)
</details>

## Question 9
You want to generate documentation for a Pulumi infrastructure codebase. The docs should include architecture diagrams in Mermaid format, but only when Claude detects complex multi-service topologies (more than 4 resources with cross-dependencies). You want this rule to apply automatically without developer intervention. How do you express this?

A) Add the condition to CLAUDE.md as a prose rule: "When generating docs for Pulumi files, include Mermaid diagrams if the topology has >4 cross-dependent resources."
B) Create a `.claude/rules/` file with `globs: ["**/*.ts", "**/*.py"]` and embed the Mermaid condition in the rules body so it activates on all IaC files.
C) Create a `/docs-infra` skill that engineers invoke manually; the skill includes the Mermaid condition internally.
D) Add the rule to `~/.claude/CLAUDE.md` so it applies globally across all projects and all IaC documentation tasks.

<details><summary>Answer</summary>
**A)** Behavioral rules with conditional logic expressed in natural language in CLAUDE.md are the right mechanism. Claude can interpret the condition ("more than 4 cross-dependent resources") and apply it at generation time without manual triggers. B is wrong because glob rules activate based on file path, not content analysis — the rule would fire for all TS/Python files, not just complex topologies. C is wrong because skill invocation is manual and doesn't satisfy "automatically without developer intervention." D is wrong because global user CLAUDE.md pollutes all projects, not just this one. (source: CLAUDE.md guide)
</details>

## Question 10
Your team uses a monorepo with a `/generate-service` slash command defined in `.claude/skills/generate-service.md`. A new team member wants to use the same skill but with their personal company-name prefix in all generated files. They add their own version to `~/.claude/skills/generate-service.md`. Which statement is true?

A) Claude will merge both skill definitions, using the project version for shared rules and the personal version for personal preferences.
B) The personal version takes precedence because user-level config is loaded after project config and therefore wins.
C) Claude detects the name collision and prompts the engineer to choose which version to run each time.
D) The personal skill at `~/.claude/skills/generate-service.md` will be silently shadowed by the project version; the personal modifications will never run.

<details><summary>Answer</summary>
**D)** Project-scoped skills take precedence over personal skills with the same name. The personal `~/.claude/skills/generate-service.md` is silently shadowed. B is wrong because project config wins on name collision — user config does not take precedence for skills. A is wrong because Claude does not merge skill definitions. C is wrong because there is no interactive disambiguation prompt; the resolution is silent and deterministic. The developer should use a unique name like `/my-generate-service` for their variant. (source: Claude Code skills documentation)
</details>

## Question 11
You are generating a comprehensive test suite for a Python Flask API with 23 endpoints. After Claude generates 180 test functions, you run pytest and discover 12 tests fail due to incorrect mock configurations. What is the best retry strategy?

A) Delete all generated tests and ask Claude to regenerate from scratch with an instruction to "write correct mocks."
B) Pass the failing test output and error messages back to Claude with instructions to fix only the failing tests, preserving the passing ones.
C) Increase the model temperature setting to get more varied mock configurations on the next generation attempt.
D) Regenerate only the mock configuration files separately, then manually splice them into the failing test functions.

<details><summary>Answer</summary>
**B)** Targeted repair — passing failure output back to Claude and asking it to fix only the failures — is the most efficient strategy. It preserves 168 passing tests, provides concrete error signals, and avoids unnecessary re-generation. A is wrong because deleting everything discards working tests and loses information. C is wrong because temperature affects randomness, not correctness — higher temperature would make mock configurations less predictable, not more accurate. D is wrong because mock configuration is embedded in test logic; manual splicing is error-prone and time-consuming. (source: Claude Code best practices)
</details>

## Question 12
You want to use Claude Code to generate Terraform for a production AWS environment. The scope includes 12 new resources, 3 IAM policy updates, and deletion of 2 deprecated security groups. Before Claude writes any files, you want to review and approve the full plan. What is the correct approach?

A) Set `autoApprove: false` in `.claude/settings.json` so Claude prompts before every individual tool call.
B) Run Claude in read-only mode initially, then switch to write mode after reviewing its analysis.
C) Ask Claude to generate a `CHANGES.md` document first, review it, then ask Claude to proceed with file generation.
D) Use plan mode to have Claude produce a complete plan of all changes first, review it, then approve execution.

<details><summary>Answer</summary>
**D)** Plan mode is specifically designed for this use case: Claude produces a complete plan of proposed changes before any execution, and the developer approves before anything is written. A is wrong because per-call approval interrupts execution at every tool invocation, not at the plan level — it is disruptive without giving a holistic view. B is wrong because "read-only mode" is not a built-in Claude Code mode. C is wrong because asking Claude to write a CHANGES.md first is a workaround, not the intended mechanism — plan mode serves this purpose natively. (source: Plan mode documentation)
</details>

## Question 13
Your React frontend codebase has a `src/components/` library and a `src/pages/` directory. Components must use the company design system and must never import from `src/pages/`. Pages can import from `src/components/`. You want these rules enforced automatically during code generation. What is the best approach?

A) Use two `.claude/rules/` files: one with `globs: ["src/components/**"]` containing the component-layer rules, another with `globs: ["src/pages/**"]` for page rules.
B) Add an ESLint rule to `eslint.config.js` and instruct Claude to run the linter after every generation; Claude will self-correct on lint failure.
C) Add both rules to the root CLAUDE.md so they apply globally to all file generations in the project.
D) Create a pre-tool hook in `.claude/settings.json` that inspects every `Edit` call and rejects writes that violate the import structure.

<details><summary>Answer</summary>
**A)** Two glob-scoped rules files apply the right constraints to the right paths automatically. Component rules only fire for `src/components/**`; page rules only fire for `src/pages/**`. C is wrong because putting both rules in root CLAUDE.md applies them globally — the component-only restriction would incorrectly apply to page files. B is wrong because relying on a linter as the primary enforcement means Claude may generate the wrong code first and only fix it post-lint; rules prevent the error upfront. D is wrong because a pre-tool hook for import inspection would require custom logic and is more complex than path-scoped rules. (source: Claude Code settings)
</details>

## Question 14
You have a Claude Code skill at `.claude/skills/db-migrate.md` that generates SQLAlchemy migration files. A teammate complains that when they invoke `/db-migrate`, Claude also pulls in context from the current frontend CLAUDE.md rules and generates irrelevant React import patterns in the migration output. What is the minimum change to fix this?

A) Add `context: fork` to the skill's frontmatter so it runs in an isolated sub-agent without inheriting the active session's accumulated context.
B) Move the skill to `~/.claude/skills/` so it runs outside the project context entirely and ignores project CLAUDE.md.
C) Add a `context: clear` directive inside the skill body to flush all inherited context before the skill executes.
D) Instruct the teammate to close and reopen their Claude Code session before invoking `/db-migrate` to reset context state.

<details><summary>Answer</summary>
**A)** `context: fork` in skill frontmatter runs the skill in an isolated sub-agent context, preventing the main session's accumulated context (including frontend rules) from bleeding into the migration generation. B is wrong because moving to `~/.claude/skills/` changes ownership but doesn't isolate execution context. C is wrong because `context: clear` is not a valid skill directive. D is wrong because reopening a session is a workaround that doesn't solve the structural problem — the issue would recur as soon as frontend files are touched again. (source: Claude Code skills documentation)
</details>

## Question 15
You are generating API client code from an OpenAPI spec. Claude generates a working Python client, but all method names use `camelCase` instead of the `snake_case` convention required by your codebase. You want to prevent this on future generations without manually correcting every run. What is the most durable fix?

A) Add `"Use snake_case for all Python method names"` to the project CLAUDE.md so the rule persists across sessions automatically.
B) Prepend the naming constraint to your prompt each time you invoke the generation task as a reminder.
C) Create a post-generation hook that runs a `sed` command to convert camelCase to snake_case in generated files.
D) Add a comment at the top of the OpenAPI spec file instructing Claude to use snake_case when generating clients.

<details><summary>Answer</summary>
**A)** Adding the naming convention to CLAUDE.md is the most durable fix — it persists across all sessions, applies to all developers, and doesn't require manual prompt augmentation each time. B is wrong because prompt-level reminders are fragile: they're forgotten, vary between developers, and don't persist. C is wrong because a post-generation hook is a workaround that fixes symptoms, not the root cause — Claude still generates the wrong names and the hook may introduce bugs in complex names. D is wrong because OpenAPI spec comments are not a Claude Code configuration mechanism; Claude may not reliably read them as behavioral instructions. (source: CLAUDE.md guide)
</details>

## Question 16
A DevOps team wants to share a `/provision-env` skill that runs Terraform and then configures Kubernetes manifests. The skill contains sensitive logic including internal cluster endpoint patterns. They want all team members to have access but external contributors to be blocked. Where should the skill file live?

A) `~/.claude/skills/provision-env.md` on each developer's machine, distributed via an internal dotfiles repo.
B) A public skills registry entry with an access token requirement that external contributors cannot obtain.
C) `.claude/skills/provision-env.md` in the project repo, with the repo itself access-controlled to team members only.
D) The project's root `CLAUDE.md` with the skill logic embedded as a custom command section.

<details><summary>Answer</summary>
**C)** Project-scoped skills in `.claude/skills/` are the right home for team-shared skills. Access control is managed at the repository level — only people with repo access can use the skill. A is wrong because distributing via dotfiles repos is fragile: it requires each developer to manually sync and is not enforced automatically. B is wrong because there is no built-in public skills registry with access token authentication in Claude Code. D is wrong because CLAUDE.md is for context and instructions, not executable skill definitions; embedding skill logic there is not the intended pattern. (source: Claude Code skills documentation)
</details>

## Question 17
You are generating SQL queries for a complex analytics pipeline. The queries involve 6-table joins on a data warehouse with a non-obvious partitioning scheme. Claude generates syntactically valid SQL but misses partition pruning, causing full table scans. What prompt engineering approach best addresses this?

A) Ask Claude to "write efficient SQL" and rely on its training knowledge of SQL optimization patterns.
B) Ask Claude to generate the query and then ask a follow-up: "Now add partition pruning." in a second turn.
C) Add `sql-expert: true` to CLAUDE.md so Claude enables its internal SQL optimization mode.
D) Include in your prompt: the table schemas, partition key definitions, example of a correctly pruned query, and explicit instruction to always filter on partition keys.

<details><summary>Answer</summary>
**D)** Providing schemas, partition key definitions, a concrete correct example (few-shot), and an explicit constraint is the most effective prompt engineering approach for domain-specific correctness. A is wrong because "write efficient SQL" is too vague — Claude's training knowledge won't infer your specific partitioning scheme without it. B is wrong because two-turn correction works but is less efficient and less reliable than front-loading the constraints; the first generation is likely to be wrong. C is wrong because `sql-expert` is not a valid CLAUDE.md field; it has no effect. (source: Prompt engineering best practices)
</details>

## Question 18
Your team's Claude Code project has `.claude/settings.json` with `Bash` in the allowlist. A security review flags that `Bash` with no subcommand restrictions allows `rm -rf` and network exfiltration commands. What is the correct remediation?

A) Remove `Bash` from the allowlist entirely; developers must approve every shell command manually.
B) Add `rm` and `curl` to a separate denylist in `settings.json` to block the most dangerous subcommands while keeping broad Bash access.
C) Replace the broad `Bash` allowlist entry with specific `Bash(npm:*)`, `Bash(pytest:*)`, and `Bash(git:*)` entries that cover only legitimate workflows.
D) Add a pre-tool hook that pipes every `Bash` command through a regex filter before execution.

<details><summary>Answer</summary>
**C)** Replacing the broad `Bash` allowlist entry with specific `Bash(command:*)` patterns is the correct principle of least privilege approach. Only approved subcommands run without approval; anything else requires manual confirmation. A is wrong because removing `Bash` entirely breaks legitimate workflows and creates constant interruption. B is wrong because a denylist is incomplete — it only blocks known bad commands but allows any other dangerous command not on the list. D is wrong because a regex-based pre-tool hook is custom logic that is fragile, incomplete, and not the intended settings mechanism. (source: Claude Code settings)
</details>

## Question 19
You are generating a Go microservice from scratch. You want Claude to follow your team's project structure: `cmd/`, `internal/`, `pkg/`, and `api/` directories with specific file placement conventions. You have a reference service already structured correctly at `services/user-service/`. What is the most efficient way to inject this structural knowledge?

A) Describe the project structure in the CLAUDE.md using prose: "Use cmd/ for entry points, internal/ for private code, etc."
B) Include the directory tree output (`tree services/user-service/`) in your generation prompt each time as inline context.
C) Create a `.claude/rules/` file with `globs: ["services/**"]` that describes the Go project structure conventions.
D) Use `@services/user-service/` as an import directive in CLAUDE.md so Claude can read the reference structure dynamically.

<details><summary>Answer</summary>
**D)** The `@path/` import directive in CLAUDE.md allows Claude to dynamically read the reference service's actual structure, giving it concrete examples rather than abstract descriptions. This is more accurate and maintainable than prose. A is wrong because prose descriptions of directory structure are less precise than an actual reference — they can be misinterpreted or become stale. B is wrong because including the tree in every prompt is manual, repetitive, and doesn't persist across sessions. C is wrong because a rules file describes constraints but doesn't give Claude the concrete reference structure to model the new service after. (source: CLAUDE.md guide)
</details>

## Question 20
A developer reports that after using Claude to refactor a Go service's database layer, several integration tests that call `UserRepository.GetByEmail()` started failing. Claude only updated the method implementation but missed 4 test files that mock the interface. What workflow change would have caught this before commit?

A) Use plan mode before the refactor so Claude lists all files that reference `GetByEmail` and confirms the edit scope.
B) Ask Claude to generate a dependency graph first, then approve the graph before any refactoring begins.
C) Add a post-commit hook that runs `grep -r GetByEmail` to detect unfixed references after the commit.
D) Break the refactor into two tasks: one for implementation, one for tests — and run them as separate Claude sessions.

<details><summary>Answer</summary>
**A)** Plan mode would have revealed the full set of files referencing `GetByEmail` before any edits were made, allowing the developer to confirm the complete scope. B is wrong because generating a separate dependency graph is a workaround — plan mode is the built-in mechanism for scope review. C is wrong because a post-commit hook runs after the damage is done; it catches the problem too late. D is wrong because splitting into two sessions doesn't guarantee the second session finds all references — plan mode's holistic scope review is more reliable. (source: Plan mode documentation)
</details>

## Question 21
Your team is building a documentation generation tool: Claude reads Python source files and generates Sphinx-compatible RST documentation. You want to ensure Claude always generates the correct RST directive syntax (e.g., `.. autofunction::` vs `.. autoclass::`) without drift across team members. What is the most reliable approach?

A) Add an RST syntax reference section to the project CLAUDE.md with the correct directive formats and examples.
B) Create a `/gen-docs` skill that includes the RST syntax examples in its body, invoked explicitly for documentation tasks.
C) Trust Claude's training knowledge of Sphinx RST format; add a note in the PR template to review directive syntax.
D) Add a post-generation hook that runs `sphinx-build` and pipes errors back to Claude for self-correction.

<details><summary>Answer</summary>
**A)** Including RST directive examples directly in the project CLAUDE.md ensures every team member's Claude session has the correct syntax available without manual invocation. It also persists across sessions and new developers automatically get the correct rules. B is wrong because a skill requires explicit invocation — developers who forget to run `/gen-docs` first will not get the directive examples. C is wrong because trusting training knowledge is fragile for specific framework versions; relying on PR review is too late in the process. D is wrong because running `sphinx-build` as a correction loop is expensive for a problem that can be prevented by providing the correct syntax upfront. (source: CLAUDE.md guide)
</details>

## Question 22
You are using Claude Code to explore an unfamiliar microservices codebase with 30+ services before writing any code. You want Claude to map service dependencies and identify which services call the auth service. Which approach is most appropriate?

A) Ask Claude to directly read every `main.go` file across all services to find auth service imports.
B) Ask Claude to run `grep -r "auth-service"` across the repo and review the matches manually.
C) Use a subagent with `context: fork` for the exploration phase so the dependency map is computed in isolation and a summary is returned to the main session.
D) Create a CLAUDE.md entry listing all 30 services so Claude has the full dependency map pre-loaded.

<details><summary>Answer</summary>
**C)** A forked subagent is ideal for broad codebase exploration: it performs the investigative work in isolation, returns a clean summary to the main session, and prevents exploration noise from consuming the main context window for subsequent implementation work. A is wrong because directly reading every `main.go` in the main session consumes context on exploratory output that may be redundant for the actual task. B is wrong because `grep` output is useful but dumping it into the main session context is less targeted than a subagent-produced summary. D is wrong because manually curating a 30-service dependency map in CLAUDE.md is a maintenance burden and quickly becomes stale. (source: Claude Code subagent documentation)
</details>

## Question 23
A teammate creates a custom `/sql-review` skill that internally invokes `/format-sql` (another team skill) for syntax formatting before reviewing query logic. The `/format-sql` skill is defined in `.claude/skills/format-sql.md`. When `/sql-review` calls it, which statement is true?

A) Skills cannot call other skills; `/sql-review` must inline the formatting logic from `/format-sql` to function correctly.
B) `/format-sql` always runs in an isolated sub-agent when called from another skill, regardless of frontmatter settings.
C) `/sql-review` can invoke `/format-sql` via a skill composition pattern, and the called skill runs in the same context unless `context: fork` is specified.
D) Calling one skill from another creates a circular dependency risk that Claude Code detects and blocks at load time.

<details><summary>Answer</summary>
**C)** Skill composition — one skill invoking another — is supported. The called skill runs in the same session context by default; adding `context: fork` to the called skill's frontmatter would isolate it. A is wrong because skill composition is a valid pattern; inlining is not required. B is wrong because sub-agent isolation is not automatic — it requires explicit `context: fork`. D is wrong because circular dependency detection is not a described load-time behavior; skills are loaded on demand, not pre-analyzed for circular calls. (source: Claude Code skills documentation)
</details>

## Question 24
You want to use Claude Code to generate Pulumi TypeScript stacks. Your CLAUDE.md currently has instructions for both frontend React work and infrastructure. A developer working exclusively on infrastructure complains that Claude keeps suggesting React-style component patterns in Pulumi resource definitions. What is the most targeted fix?

A) Create separate skills `/react-context` and `/infra-context` that developers invoke to switch between domain contexts.
B) Create a separate CLAUDE.md in the `infra/` subdirectory with only infrastructure rules so context is restricted when working in that directory.
C) Remove the React rules from the root CLAUDE.md entirely to eliminate the contamination at the source.
D) Move the infrastructure rules to a `.claude/rules/` file with `globs: ["infra/**"]` so they only activate for infrastructure file paths.

<details><summary>Answer</summary>
**D)** Moving infrastructure rules to a glob-scoped rules file ensures they activate only when working in `infra/**` paths, and React rules can similarly be scoped to `src/**`. This surgically separates the two domains without deleting shared context. A is wrong because manual skill invocation is fragile and adds friction; glob rules activate automatically. B is wrong because a subdirectory CLAUDE.md does work but is less flexible than glob rules — it requires the developer to be in that directory and doesn't interact cleanly with multi-file operations. C is wrong because removing React rules entirely breaks frontend development for the rest of the team. (source: Claude Code settings)
</details>

## Question 25
Your Python data pipeline uses `pandas`, `dask`, and `sqlalchemy`. You want Claude to use `dask` for operations on DataFrames larger than 10 GB and `pandas` for smaller ones, but only when generating ETL processing modules. How do you express this rule most precisely?

A) Add the rule to root CLAUDE.md: "Use dask for DataFrames >10 GB, pandas otherwise." — it will apply to all Python files globally.
B) Add the rule to a `/generate-etl` skill so it is enforced only when that specific skill is invoked for ETL generation.
C) Create a `.claude/rules/` file with `globs: ["src/etl/**/*.py"]` containing the dask/pandas sizing rule so it activates only for ETL module paths.
D) Include a comment in every ETL file: `# Claude: use dask for large DataFrames` as an inline instruction.

<details><summary>Answer</summary>
**C)** A glob-scoped rules file targeting `src/etl/**/*.py` activates the dask/pandas rule automatically for ETL modules without affecting other Python files. A is wrong because adding the rule to root CLAUDE.md applies it globally — Claude might incorrectly apply it to non-ETL Python files like Flask route handlers. B is wrong because skill enforcement requires manual invocation and doesn't apply to arbitrary edits within ETL files. D is wrong because inline file comments are not a Claude Code configuration mechanism; they may be inconsistently followed and are not the intended pattern. (source: Claude Code settings)
</details>

## Question 26
You've generated a React component with Claude that renders a paginated data table. You want to verify it actually works — not just that it compiles — before merging. What is the most reliable verification approach?

A) Ask Claude to review the generated component code and confirm it is logically correct.
B) Run the component in a test environment using a verification tool or automated browser test, and observe actual rendered behavior.
C) Write unit tests with Claude and check that the tests pass as a proxy for functional correctness.
D) Ask Claude to generate a checklist of potential bugs and manually review each item before merging.

<details><summary>Answer</summary>
**B)** Running the component in a real environment and observing rendered behavior is the most reliable verification — it catches rendering bugs, runtime errors, and UX issues that static analysis and unit tests miss. A is wrong because Claude reviewing its own code is prone to confirming false assumptions — it tends to miss its own blind spots. C is wrong because unit tests are valuable but test the model, not the actual rendered output; pagination bugs often appear in DOM interactions, not unit-testable logic. D is wrong because a self-generated bug checklist is again Claude auditing its own work, which is less reliable than empirical observation. (source: Claude Code best practices)
</details>

## Question 27
Your team wants to add a pre-commit validation that runs `terraform validate` before any Terraform files are committed when Claude Code is the author. You want this to run automatically without developer manual steps. What is the correct implementation?

A) Add `terraform validate` to the CLAUDE.md as an `always-run` directive so Claude executes it before completing any Terraform-related response.
B) Configure a `PostToolUse` hook in `.claude/settings.json` triggered on `Edit` calls to `*.tf` files that runs `terraform validate`.
C) Create a Git pre-commit hook in `.git/hooks/pre-commit` that runs `terraform validate`; this applies to all commits including Claude's.
D) Add `validateOnSave: terraform validate` to `.claude/settings.json` so Claude runs validation after saving Terraform files.

<details><summary>Answer</summary>
**B)** A `PostToolUse` hook in `.claude/settings.json` on `Edit` calls matching `*.tf` files runs `terraform validate` automatically after each Terraform edit by Claude Code. This is the native Claude Code mechanism. A is wrong because `always-run` is not a valid CLAUDE.md directive — CLAUDE.md provides context, not executable triggers. C is wrong because `.git/hooks/pre-commit` runs at commit time, not at edit time, and doesn't provide feedback during generation. D is wrong because `validateOnSave` is not a valid `settings.json` field. (source: Claude Code settings)
</details>

## Question 28
A data scientist wants Claude to generate a complete scikit-learn pipeline including preprocessing, feature engineering, and model training for a new classification task. The generated pipeline will be used in production. The scope is novel and the correct feature engineering steps are uncertain. What approach is most appropriate?

A) Use direct execution with auto-approve — the code is Python and unlikely to cause system damage even if incorrect.
B) Use plan mode so Claude proposes the complete pipeline architecture (preprocessing choices, feature steps, model selection rationale) before writing any code.
C) Ask Claude to generate the full pipeline in one shot, then review and iterate based on what was produced.
D) Break the task into three separate sessions: one for preprocessing, one for feature engineering, one for model training.

<details><summary>Answer</summary>
**B)** Plan mode is appropriate here because the scope is novel and the correct approach is uncertain — reviewing the proposed architecture before code generation allows the data scientist to validate feature engineering choices without wading through hundreds of lines of implementation. A is wrong because "unlikely to cause system damage" is not the only criterion for skipping plan mode; uncertain scope and novel tasks also warrant upfront planning. C is wrong because generating and then iterating is less efficient than reviewing a plan first for uncertain scope tasks. D is wrong because splitting into three sessions adds coordination overhead and breaks the architectural coherence of the pipeline. (source: Plan mode documentation)
</details>

## Question 29
Your team has a personal `~/.claude/CLAUDE.md` with instructions like "prefer verbose variable names" and "always add type hints." The project has a `.claude/rules/` file targeting `src/**` that says "use single-letter loop variables for performance-critical loops." A developer notices Claude is using verbose names even in the tight loops. Which configuration wins?

A) The personal `~/.claude/CLAUDE.md` wins because user-level config has higher precedence than project rules files.
B) The `.claude/rules/` file wins for files matching its glob (`src/**`) because project-scoped rules override user-level CLAUDE.md for in-scope paths.
C) Both configurations apply simultaneously and Claude attempts to satisfy both by using moderately descriptive variable names.
D) Neither wins definitively; Claude's behavior is non-deterministic when user and project rules conflict.

<details><summary>Answer</summary>
**B)** Project-scoped rules files take precedence over user-level CLAUDE.md for files matching the glob pattern. When working in `src/**`, the `.claude/rules/` instruction for single-letter loop variables should override the personal preference. A is wrong because user config does not override project config — the precedence is the opposite for in-scope path rules. C is wrong because Claude Code does not attempt to synthesize a middle ground between conflicting instructions; the more specific scoped rule wins. D is wrong because the resolution is deterministic based on scope specificity, not random. (source: CLAUDE.md guide)
</details>

## Question 30
Your organization manages 15 Claude Code projects. You want a set of universal code quality rules to apply across all projects — no test functions shorter than 3 lines, always log errors before rethrowing, always close resources in finally blocks. Where is the correct single place to configure these?

A) Commit a shared `rules.md` to a central tools repo and instruct each project's CLAUDE.md to import it via `@https://internal.example.com/rules.md`.
B) Add the rules to `~/.claude/CLAUDE.md` on each developer's machine so they apply to all projects that developer works on.
C) Create an organization-level CLAUDE.md in a parent directory above all 15 project directories so it is inherited by all projects.
D) Add the rules to `.claude/settings.json` in each project under a `globalRules` field that Claude Code reads automatically.

<details><summary>Answer</summary>
**B)** `~/.claude/CLAUDE.md` is the user-level global config that applies to all Claude Code sessions on that machine, making it the correct location for universal rules that span all projects. A is wrong because remote `@URL` imports are not a supported CLAUDE.md directive format; CLAUDE.md supports local `@path/to/file` imports only. C is wrong because there is no CLAUDE.md inheritance from parent directories above the repo root; each project's CLAUDE.md is scoped to its own repo. D is wrong because `globalRules` is not a valid `settings.json` field; settings.json manages tool permissions and hooks, not global instruction rules. (source: CLAUDE.md guide)
</details>
