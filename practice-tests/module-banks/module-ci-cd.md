# Module Bank: Claude Code for CI/CD

Auto-generated bank with 30 questions.

## Question 1
Your mobile app CI pipeline builds Android and iOS variants in parallel. Each variant produces a build log you want Claude to analyze for deprecation warnings. The build takes 12 minutes; the analysis is not blocking any developer. You want to cut analysis costs. Which approach is correct?

A) Use the synchronous API for each variant analysis so results arrive immediately and can be merged into a single report before the build artifact is uploaded
B) Use the Message Batches API to submit both analyses together, collecting results asynchronously since no developer is blocked on the output
C) Use the synchronous API because the Message Batches API does not support multi-item submissions from the same pipeline run
D) Use the Message Batches API for the iOS variant only, since Android builds are typically faster and their analysis must complete before artifact signing

<details><summary>Answer</summary>
**B)** Both analyses are latency-tolerant post-build background work with no developer waiting on them. The Message Batches API delivers ~50% cost savings for exactly this pattern: fire-and-forget, non-blocking, deferred result collection. A is wrong because synchronous routing wastes ~50% cost on work nobody is waiting for. C is wrong because the Batches API explicitly supports submitting multiple requests in a single batch. D is wrong because there is no documented requirement to sequence Android and iOS analyses; signing depends on the artifact, not the analysis result. (source: Message Batches API)
</details>

## Question 2
A Terraform infrastructure-as-code pipeline runs Claude to validate plan output before `terraform apply`. The pipeline blocks apply until validation completes. A DevOps engineer proposes switching to the Message Batches API to reduce costs by ~50%. Should you make the switch?

A) Yes — the ~50% savings always justify the switch, and the apply step can be designed to poll for the batch result before proceeding
B) Yes — Message Batches API still supports fast responses for short prompts, so the blocking latency impact would be negligible
C) No — the Message Batches API is fire-and-forget with up to 24-hour processing time; a blocking gate requires a synchronous response
D) No — Terraform plan output often exceeds the token limits of the Message Batches API, making it unsuitable for IaC validation

<details><summary>Answer</summary>
**C)** When a pipeline step is blocking (apply cannot proceed without the validation result), it requires a synchronous response. The Message Batches API offers no latency guarantee — processing can take up to 24 hours — which would stall the deployment pipeline indefinitely. A is wrong because polling for a batch result on a blocking gate defeats the purpose and introduces unpredictable delay. B is wrong because the Batches API has no fast-path for short prompts; latency is undefined. D is wrong because the Batches API has the same token limits as the synchronous API. (source: Message Batches API)
</details>

## Question 3
A nightly pipeline runs Claude against every merged PR from the past week to generate a changelog draft. Each PR produces one Claude request. The team processes roughly 200 PRs per week. Which API approach minimizes cost with acceptable trade-offs?

A) Synchronous API with a concurrency limit of 5 parallel requests to avoid rate limiting
B) Message Batches API to submit all 200 requests in one or more batches, collecting results the following morning
C) Synchronous API because 200 requests per week is too small a volume to justify the operational overhead of managing batch job state
D) Message Batches API for PRs with more than 10 file changes; synchronous API for smaller PRs to balance latency and cost

<details><summary>Answer</summary>
**B)** A weekly nightly run generating changelog drafts is the ideal Message Batches use case: latency-tolerant, non-blocking, scheduled work. Submitting all 200 as a batch captures ~50% cost savings with no impact on any developer workflow. A loses the ~50% savings for no benefit since nobody is waiting overnight. C is wrong — 200 requests/week is precisely the volume where batch savings add up meaningfully, and batch job state management is simple (poll once the next morning). D is wrong because splitting by file count adds complexity without a principled reason; the latency tolerance applies to all 200. (source: Message Batches API)
</details>

## Question 4
A CI pipeline uses Claude with iterative tool-calling to traverse a dependency graph: Claude calls a `resolve_package` tool, receives the result, calls it again for transitive deps, and repeats until the full tree is resolved. The team wants to cut costs by moving this to the Message Batches API. Is this feasible?

A) Yes — submit the initial request as a batch item; when it returns with tool call results, submit the next batch item to continue the chain
B) Yes — the Message Batches API supports streaming partial results, so tool calls can be intercepted mid-batch and resolved by the CI server
C) No — the Message Batches API does not support mid-request tool interception; iterative tool-calling requires a synchronous back-and-forth loop
D) No — tool use is disabled in the Message Batches API regardless of the use case or model version

<details><summary>Answer</summary>
**C)** Iterative tool-calling requires the client to receive a tool_use block, call the external tool, and send the result back before Claude continues. The Message Batches API is fire-and-forget with no mid-request interception; it cannot pause a batch item to wait for an external tool response. A is wrong because re-submitting follow-up batch items works only for independent requests, not for a stateful multi-turn conversation that depends on the previous turn's tool results. B is wrong because the Batches API does not support streaming. D overstates the restriction — tool use definitions can be included, but the iterative loop pattern specifically cannot work in batch mode. (source: Message Batches API)
</details>

## Question 5
A release pipeline has two post-merge stages: (1) a 2-minute lightweight lint check that generates inline PR comments a developer must acknowledge before the branch is marked clean, and (2) a full container image vulnerability scan that runs after merge and emails a security summary report. Which API routing is correct?

A) Synchronous for both — keeping consistent API usage simplifies the pipeline and avoids managing two polling loops
B) Message Batches for both — both stages run post-merge so neither is strictly blocking developer action
C) Synchronous for stage 1; Message Batches for stage 2 — the developer must acknowledge stage 1 findings before the branch is marked clean, making it blocking; stage 2 is an async report
D) Message Batches for stage 1; synchronous for stage 2 — vulnerability findings are high-severity and should be delivered as fast as possible

<details><summary>Answer</summary>
**C)** Stage 1 requires a developer to read and acknowledge findings before the branch clears — that is a blocking human-in-the-loop gate requiring a synchronous response. Stage 2 produces an email report with no human waiting synchronously; the ~50% batch savings apply cleanly. A loses the cost savings on stage 2 for no benefit. B is wrong because stage 1 does block the developer (they must acknowledge before the branch is marked clean). D reverses the routing: stage 1 cannot tolerate batch latency since a developer is waiting; stage 2 has no interactive recipient. (source: Message Batches API)
</details>

## Question 6
You integrate Claude into a GitHub Actions workflow to review database migration files before they are applied. The job runs `claude "Review this migration for data-loss risks"` and the process hangs indefinitely. The workflow has `ANTHROPIC_API_KEY` set correctly. What is the most likely cause and fix?

A) The API key lacks write permission; add the `migrations:read` scope to the key and retry
B) The `claude` command is missing the `-p` flag; without it the CLI waits for interactive input even in a non-TTY environment
C) GitHub Actions does not allocate a pseudo-TTY by default; add `shell: bash --login` to the step to fix TTY allocation
D) The migration file is too large for inline prompt injection; use `--file` to stream it instead of embedding it in the prompt string

<details><summary>Answer</summary>
**B)** Without `-p` / `--print`, the Claude Code CLI enters interactive mode and waits for further input from the user, hanging indefinitely in a CI environment with no TTY. The fix is `claude -p "Review this migration for data-loss risks"`. A is wrong because the API key scope for Claude is not broken into sub-permissions like `migrations:read`. C is wrong because the issue is the CLI's interactive mode, not TTY allocation — `bash --login` would not change Claude's behavior. D is wrong because `--file` is not a documented Claude Code CLI flag for streaming file content. (source: Claude Code CLI reference)
</details>

## Question 7
A CI step runs `claude -p "Generate release notes from this diff"` and pipes the output to a shell script that extracts the version number using regex. The regex breaks whenever Claude changes its phrasing. What is the most robust fix?

A) Pin the Claude model version in the API call so output format does not change across model upgrades
B) Add "respond only in plain text, no markdown" to the prompt to eliminate formatting variability
C) Replace the natural-language prompt with a structured output contract: instruct Claude to return JSON with a `version` field, then parse the JSON in the script
D) Add a second Claude call that takes the first output and reformats it into a consistent template before the regex runs

<details><summary>Answer</summary>
**C)** Regex over natural language output is inherently fragile because LLM phrasing varies. Defining a structured output contract (e.g., `{"version": "2.4.1", "notes": "..."}`) and parsing JSON is robust and survives rephrasing. A is wrong because even a pinned model may vary phrasing across requests. B reduces some variability but "plain text, no markdown" still allows Claude to phrase the version in many ways that break a specific regex. D adds cost and latency to work around a problem that structured output solves directly. (source: Prompt engineering)
</details>

## Question 8
A documentation generation pipeline runs Claude to produce API reference docs from OpenAPI spec files. The output includes section headers, but their capitalization style varies across runs (e.g., "Authentication Methods" vs "authentication methods" vs "Authentication methods"). A downstream renderer depends on consistent casing. What prompt engineering technique best stabilizes this?

A) Add a sentence to the prompt: "Capitalize section headers consistently"
B) Provide 3–4 few-shot examples in the prompt that demonstrate exactly the expected capitalization style for headers
C) Post-process the output with a Python `str.title()` call to normalize all headers after generation
D) Enable `temperature=0` in the API call to make output fully deterministic

<details><summary>Answer</summary>
**B)** Few-shot examples are the most reliable way to establish a consistent formatting convention in LLM output. Showing Claude concrete examples of the expected style anchors the behavior more strongly than a verbal instruction. A is wrong because "capitalize consistently" is ambiguous — it does not specify which style (title case, sentence case, all-caps). C is wrong because `str.title()` would corrupt headers like "OAuth2" or "HTTP/2" and does not apply to headers that appear mid-sentence. D is wrong because temperature=0 reduces randomness but does not define which casing convention Claude should follow. (source: Prompt engineering)
</details>

## Question 9
A performance regression detection pipeline runs Claude on benchmark result diffs. In the first week, Claude repeatedly flags the same cold-start latency increase that the team already acknowledged and accepted. How should you modify the pipeline to stop these repeat findings?

A) Add a rule to the post-processing script to filter any finding that contains the word "cold-start"
B) Inject the list of previously acknowledged findings into the prompt context so Claude knows which regressions have already been reviewed and accepted
C) Increase the confidence threshold so only severe regressions above 30% degradation are reported
D) Switch to a two-pass architecture where the first pass identifies regressions and the second pass deduplicates against a static known-issues list

<details><summary>Answer</summary>
**B)** Claude can only avoid repeating acknowledged findings if it can see what has already been accepted. Injecting prior findings as prompt context gives Claude the ground truth to reason against, directly solving the duplication problem. A is wrong because keyword filtering on "cold-start" is brittle — future cold-start regressions that should be flagged would also be suppressed. C is wrong because the threshold change would suppress legitimate regressions below 30% and does not address why acknowledged findings keep resurfacing. D is wrong because deduplication against a static list requires maintaining that list separately and still does not give Claude the context to reason about why something was accepted. (source: Prompt engineering)
</details>

## Question 10
A CI pipeline posts Claude's code review findings as PR comments. A developer notices that Claude's output sometimes contains raw Markdown backtick code blocks with unescaped HTML entities from user-supplied variable names. These get rendered unexpectedly in the GitHub PR UI. What change addresses this safely?

A) Pass `--output-format plain` to the `claude -p` invocation to strip all Markdown from the response
B) Sanitize Claude's output in the pipeline script before posting it to the GitHub PR API, escaping or stripping unsafe HTML entities
C) Add to the prompt: "Do not use HTML entities in your output" to prevent the issue at generation time
D) Switch from inline PR comments to a separate PR summary comment so HTML rendering is isolated to one location

<details><summary>Answer</summary>
**B)** Sanitizing output before posting to an external API is the correct defense-in-depth approach. Claude cannot reliably guarantee absence of user-controlled content that may contain HTML entities, so the pipeline layer must sanitize before forwarding to the GitHub API. A is wrong because `--output-format plain` is not a valid Claude Code CLI flag. C is wrong because the entities originate from user-supplied variable names in the analyzed code, not from Claude's own phrasing — a prompt instruction cannot prevent Claude from quoting code that already contains them. D is wrong because it moves the problem, not fixes it. (source: Claude Code CLI reference)
</details>

## Question 11
You want Claude Code to run in a GitHub Actions job that reviews container Dockerfiles for security best practices. The job must read findings as structured data to decide whether to fail the build. Which invocation pattern is most appropriate?

A) `claude -p "Review this Dockerfile" | jq '.findings'`
B) `claude -p "Review this Dockerfile" --output-format json` and parse the JSON `result` field in the script
C) `claude -p "Review this Dockerfile" --output-format stream-json` and accumulate the streamed JSON lines until the `result` event appears
D) `claude -p "Review this Dockerfile" --json` and treat each line as an independent JSON object

<details><summary>Answer</summary>
**C)** `--output-format stream-json` emits newline-delimited JSON events including a final `result` event; this is the correct machine-readable mode for CI scripts that need to parse structured output from Claude Code. B is partially right in concept but `--output-format json` is not the documented flag — the correct flag is `stream-json` for streaming or `json` depending on the CLI version, but `stream-json` is the documented CI-friendly mode. A is wrong because plain text output does not have a `.findings` JSON key to `jq` against. D is wrong because `--json` is not a valid Claude Code CLI flag. (source: Claude Code CLI reference)
</details>

## Question 12
A GitHub Actions workflow needs to limit how many tokens Claude Code can use per review to control costs. Which approach is correct for the Claude Code CLI?

A) Pass `--max-tokens 2000` to the `claude -p` invocation to cap the response length
B) Set the `CLAUDE_CODE_MAX_OUTPUT_TOKENS` environment variable in the workflow step before invoking `claude -p`
C) Add `max_tokens: 2000` to a `.claude-ci-config.yml` file in the repository root so it is auto-loaded
D) Use the `--budget 2000` flag to set a combined input+output token budget for the session

<details><summary>Answer</summary>
**B)** `CLAUDE_CODE_MAX_OUTPUT_TOKENS` is the documented environment variable for controlling maximum output token count in Claude Code CLI invocations, making it the correct CI tuning mechanism. A is wrong because `--max-tokens` is not a documented Claude Code CLI flag; it is an API parameter, not a CLI flag. C is wrong because `.claude-ci-config.yml` is not an auto-loaded config file in Claude Code. D is wrong because `--budget` is not a valid Claude Code CLI flag. (source: Claude Code CLI reference)
</details>

## Question 13
A mobile release pipeline uses Claude to analyze crash symbolication reports after each TestFlight build. The analysis script exits with a non-zero code and the CI job fails, but the Claude output looks correct. You need to distinguish between a Claude processing error and a script logic error. What exit code indicates a Claude configuration or permission error specifically?

A) Exit code 1 — generic error covering both Claude and script failures
B) Exit code 2 — configuration or permission error from the Claude Code CLI
C) Exit code 3 — permission denied when Claude attempts to read a file outside the allowed path
D) Exit code 127 — command not found, indicating Claude Code is not installed in the CI environment

<details><summary>Answer</summary>
**B)** The Claude Code CLI uses exit code 2 specifically for configuration and permission errors, distinguishing them from general runtime errors (exit code 1). This lets CI scripts branch on the exit code to detect misconfiguration separately from processing failures. A is wrong because exit code 1 is a general error, not specific to configuration issues. C is wrong because exit code 3 is not a documented Claude Code exit code. D is correct in what it means (command not found in shell) but is a shell-level error, not a Claude Code exit code. (source: Claude Code CLI reference)
</details>

## Question 14
A team deploys Claude Code in a Jenkins pipeline on a self-hosted agent. The agent has no internet access to Claude.ai but does have access to the Anthropic API endpoint. The `claude` CLI command is available. What configuration ensures the CLI uses the API correctly in this environment?

A) Set `ANTHROPIC_BASE_URL` to point to an internal proxy that forwards to `api.anthropic.com`
B) Set `ANTHROPIC_API_KEY` in the agent environment — the CLI uses the API endpoint directly and does not require claude.ai access
C) Add `--no-web` to the `claude -p` invocation to disable browser-based authentication flows
D) Configure `CLAUDE_CODE_USE_BEDROCK=1` to route through AWS Bedrock instead of the Anthropic API, which is accessible from the agent network

<details><summary>Answer</summary>
**B)** The Claude Code CLI authenticates via `ANTHROPIC_API_KEY` and calls the Anthropic API endpoint directly. Claude.ai (the web product) is not required for CLI operation. A is unnecessary if the agent already has direct access to `api.anthropic.com`. C is wrong because `--no-web` is not a documented CLI flag. D is wrong because Bedrock routing requires AWS credentials and Bedrock-specific configuration; it is a separate deployment path, not a fix for network access. (source: Claude Code CLI reference)
</details>

## Question 15
A CI pipeline analyzes API compatibility between two versions of a service. The prompt instructs Claude to "list breaking changes." Across 50 pipeline runs, Claude sometimes lists changes as bullets, sometimes as a numbered list, and sometimes as a prose paragraph. A downstream consumer parses the output programmatically. What is the most effective prompt fix?

A) Append "Use bullet points only" to the prompt to enforce a single list format
B) Run each analysis twice and compare outputs; use the majority format as the canonical result
C) Define an explicit JSON schema in the prompt (e.g., `{"breaking_changes": ["...", "..."]}`) and instruct Claude to return only valid JSON matching that schema
D) Add `--seed 42` to the `claude -p` invocation to make output formatting deterministic

<details><summary>Answer</summary>
**C)** Defining a JSON schema in the prompt and requiring Claude to return valid JSON matching it is the only approach that reliably enforces machine-parseable structure. A reduces variability but bullets vs prose can still vary in nesting and punctuation that breaks parsers. B doubles API cost and still does not guarantee consistent format — two inconsistent outputs produce no majority. D is wrong because `--seed` is not a documented Claude Code CLI flag. (source: Prompt engineering)
</details>

## Question 16
A security scanning pipeline flags a high number of false positives in the "hardcoded secrets" category. The team tunes the prompt by adding: "Only report findings where you are highly confident a real secret is present." After the change, the false positive rate drops from 60% to 35%, but developers still distrust the category and ignore all findings. What additional change most restores developer trust?

A) Further lower the confidence threshold by adding "Only report findings where you are certain beyond all doubt"
B) Have Claude include a brief rationale and confidence percentage for each finding so developers can triage quickly in a single pass
C) Add a second Claude review pass that independently re-scores each finding to filter out remaining false positives
D) Switch to a rule-based regex scanner for secrets detection and remove Claude from this category entirely

<details><summary>Answer</summary>
**B)** Including a rationale and confidence score per finding lets developers triage at a glance — high-confidence findings with clear reasons are acted on, and borderline ones can be reviewed with context. This restores signal without removing the category. A continues tightening verbal thresholds, which have diminishing returns at 35% FP and still give developers no basis to distinguish findings. C adds latency and cost for a second LLM pass that may not reduce FP significantly further. D abandons the AI capability entirely rather than improving trust in the output. (source: Prompt engineering)
</details>

## Question 17
An API compatibility test pipeline needs to decide which changes require a human approval gate before deployment. Claude assigns a severity field in its JSON output. The team debates whether to auto-block on severity >= "high" or require a second Claude pass to confirm. When is a second Claude pass worth the added cost and latency?

A) Always — two LLM evaluations always produce a more accurate result than one
B) When the first pass is a broad sweep (many files, low context per file) and the second pass does a focused deep-dive on candidate issues with full context
C) When the model used in the first pass is a smaller, cheaper model and the second pass upgrades to a larger model for confirmation
D) When the first pass prompt instructs Claude to reason step-by-step (chain-of-thought), making a second pass redundant

<details><summary>Answer</summary>
**B)** A multi-pass architecture earns its cost when the passes are structurally different: the first pass is a broad, cheap triage over many files and the second pass does a focused, high-context deep-dive on the candidates surfaced by the first. This delivers better accuracy than one expensive full-context pass. A is wrong because two identical passes on the same input add cost without meaningful accuracy gain. C is a valid optimization pattern but is a subset of B — the key is context depth, not just model size. D is wrong because chain-of-thought in one pass does not eliminate the benefit of a second independent focused evaluation. (source: Architecture patterns)
</details>

## Question 18
A CI pipeline reviews infrastructure Terraform modules. A single module can span 15 files. The team runs one Claude call with all 15 files concatenated. Review quality is poor for files that appear late in the context. Which architecture change addresses this?

A) Increase `CLAUDE_CODE_MAX_OUTPUT_TOKENS` to allow Claude more room to cover all files
B) Run a per-file pass first to collect per-file findings, then a second integration pass with only the cross-file summaries as context to identify integration-level issues
C) Randomize the file order on each run so no single file is always penalized by late-context attention decay
D) Split the module into separate smaller modules to reduce the number of files Claude needs to review simultaneously

<details><summary>Answer</summary>
**B)** A multi-pass architecture solves late-context degradation: each file gets a focused first-pass review, and the integration pass uses only the condensed findings (not the full source), keeping the integration context small and high-signal. A is wrong because output token count does not affect attention over input context. C is wrong because randomizing order does not fix attention degradation — it just distributes it randomly. D changes the repository structure to work around a pipeline limitation, which is the wrong layer to fix. (source: Architecture patterns)
</details>

## Question 19
A team runs Claude to review every pushed commit for security vulnerabilities. The pipeline runs cheaply but developers complain that obvious style and formatting issues are consuming finding slots that should be used for real security findings. What pipeline stage ordering change best addresses this?

A) Run both security and style checks in parallel, then merge the output and rank by severity before presenting findings
B) Run a cheap deterministic linter and formatter first; only invoke Claude for security review after linting passes, so Claude focuses exclusively on security
C) Add a prompt instruction: "Ignore style and formatting issues, focus only on security" and remove the linter from the pipeline entirely
D) Increase Claude's context window allocation so it can surface more findings per run without dropping security issues

<details><summary>Answer</summary>
**B)** Running cheap deterministic tools first (linters, formatters) filters out the noise before Claude is invoked, so Claude's attention and output budget are not wasted on issues a rule-based tool catches more cheaply and reliably. A is wrong because parallel execution still spends Claude tokens on style issues. C is wrong because removing the linter eliminates reliable, cheap style enforcement; a prompt instruction is less reliable than a dedicated tool for rule-based checks. D is wrong because adding context does not change what Claude chooses to report when both style and security issues are present. (source: Architecture patterns)
</details>

## Question 20
A new CI reviewer is added alongside an existing one. Both run Claude, but the new reviewer generates findings on code that the existing reviewer wrote in the same pipeline session. A senior engineer notices the new reviewer is systematically less critical of that code. What is the architectural cause and fix?

A) The new reviewer has a lower confidence threshold; raise its threshold to match the existing reviewer
B) Both reviewers share the same Claude session, so the new reviewer has implicit context that the code was written by the session's prior actions — use independent fresh Claude instances for reviewer roles
C) The new reviewer runs after the existing one, so it sees prior approved findings and anchors on them — reverse the execution order
D) The new reviewer's system prompt is shorter, giving it less guidance; expand the system prompt to match the existing reviewer's

<details><summary>Answer</summary>
**B)** When a reviewer and the code author share a session, the reviewer inherits in-context knowledge of the authoring decisions, which creates confirmation bias — it is less likely to critique choices it "made." The fix is the independent reviewer pattern: each reviewer is a fresh Claude instance with no session history of the code's creation. A is wrong because the issue is session context, not threshold calibration. C is wrong because execution order does not change the shared session context problem. D is wrong because system prompt length is not the cause; the session state is. (source: Architecture patterns)
</details>

## Question 21
A Kubernetes deployment pipeline stores Claude's review context in `CLAUDE.md` at the repo root. The team wants Claude to know which environments are production vs staging to avoid flagging safe staging-only configurations as production risks. Where should this context be defined, and how does Claude Code load it?

A) In a `claude-context.json` file passed via `--context-file` flag at invocation time
B) In `.claude/settings.json` under a `environments` key that Claude Code reads automatically
C) In `CLAUDE.md` at the appropriate directory level — Claude Code automatically reads `CLAUDE.md` files to inject project and directory context into the session
D) In a `SYSTEM_PROMPT.txt` file that must be passed explicitly via `--system-prompt SYSTEM_PROMPT.txt`

<details><summary>Answer</summary>
**C)** Claude Code automatically reads `CLAUDE.md` files from the current directory and parent directories to inject project context into the session. This is the designed mechanism for providing CI-specific, project-level, or directory-level context without modifying the invocation command. A is wrong because `--context-file` is not a documented Claude Code flag. B is wrong because `.claude/settings.json` manages tool permissions and settings, not free-form context injection. D is wrong because `--system-prompt` is not a documented Claude Code CLI flag for file-based system prompts. (source: Configuration and security)
</details>

## Question 22
A fintech CI pipeline stores the `ANTHROPIC_API_KEY` as a GitHub Actions secret. A security audit flags that all pipeline jobs, including documentation generation and style linting, share the same key. What is the recommended least-privilege approach?

A) Generate a separate API key for each job and store each as its own GitHub Actions secret, rotating all keys on a 90-day schedule
B) Use a single key but restrict it to specific IP addresses matching GitHub Actions runner IPs
C) Scope access by using separate keys for high-sensitivity (security review) and low-sensitivity (docs, linting) jobs, with different usage monitoring and rotation policies per tier
D) Store the API key in a `.env` file committed to the repository with restricted branch permissions

<details><summary>Answer</summary>
**C)** Tiering keys by sensitivity level is a practical least-privilege approach: high-sensitivity jobs get a tightly monitored key; low-sensitivity jobs use a separate key with lower blast radius if compromised. A is operationally correct in principle but per-job keys for docs and linting creates unnecessary management overhead. B is wrong because Anthropic does not support IP-restricted API keys as a product feature. D is wrong because committing secrets to a repository, even with branch restrictions, is a security antipattern and violates secrets management best practices. (source: Configuration and security)
</details>

## Question 23
A CI pipeline for a Python library generates documentation from docstrings using Claude. After a model update, the pipeline starts producing docs with inconsistent section ordering (Parameters before Returns in some files, reversed in others). The team wants to enforce the order without re-running failed docs manually. What is the best prompt engineering fix?

A) Add `--deterministic` to the `claude -p` invocation to lock output ordering
B) Provide a concrete few-shot example in the prompt that demonstrates exactly one function's complete documentation with Parameters then Returns in the required order
C) Add "Always output Parameters before Returns" as a bulleted rule at the end of the system prompt
D) Post-process the documentation output with a parser that reorders sections alphabetically after generation

<details><summary>Answer</summary>
**B)** A few-shot example showing the exact desired output structure anchors Claude's behavior more reliably than a textual rule. Seeing the correct section ordering demonstrated concretely is more effective than describing it. A is wrong because `--deterministic` is not a documented Claude Code CLI flag. C is a reasonable addition but verbal rules are less stable than concrete examples when formatting conventions need to be consistent across many files. D is wrong because alphabetical ordering does not match the required semantic ordering (Parameters then Returns). (source: Prompt engineering)
</details>

## Question 24
A mobile CI pipeline uses Claude to generate App Store release notes from git commit messages. Occasionally, Claude's output contains developer-internal shorthand (e.g., "fixes JIRA-4521", "reverts hotfix from staging") that should not appear in user-facing release notes. What prompt technique prevents this most reliably?

A) Post-filter the output with a regex that strips patterns matching `JIRA-\d+` and known internal terms
B) Add "Do not include internal ticket references or staging environment details" as a constraint in the prompt
C) Provide few-shot examples where commits with internal references are transformed into user-facing language that focuses on user benefit, demonstrating the desired transformation explicitly
D) Run a second Claude pass instructed to "remove internal developer references" from the first pass output

<details><summary>Answer</summary>
**C)** Few-shot examples that show the transformation from raw commits (including internal references) to clean user-facing language teach Claude the mapping concretely, covering both the inclusion rule and the tone. A handles known patterns but misses novel internal shorthand. B is a useful constraint but may not cover unfamiliar internal references Claude has not seen. D adds cost and latency for a task that well-designed few-shot examples handle in one pass. (source: Prompt engineering)
</details>

## Question 25
A CI pipeline for a multi-service monorepo runs Claude security review on every service that changed in a PR. A PR touches 8 services. The team notices each service's review mentions the same global authentication library vulnerability that was already reported and tracked. How should the pipeline reduce this redundant finding across services?

A) Deduplicate the output post-hoc using a script that detects identical finding descriptions across service reports
B) Run one review for the authentication library independently, then inject a "known tracked issues" list into each service's review prompt so Claude omits already-tracked findings
C) Add "Do not report vulnerabilities in shared libraries" to the prompt so Claude focuses only on service-specific code
D) Merge all 8 service reviews into one large prompt so Claude can self-deduplicate across services in a single pass

<details><summary>Answer</summary>
**B)** Injecting a known-issues list gives Claude the context to distinguish new findings from already-tracked ones, preventing redundant noise across all 8 service reviews. A catches exact duplicates but misses paraphrased variations of the same finding. C is wrong because suppressing all shared library findings would hide new vulnerabilities introduced in future library updates. D is wrong because merging 8 services into one prompt risks context window overflow, attention degradation across long context, and makes individual service findings harder to route. (source: Prompt engineering)
</details>

## Question 26
An iOS CI pipeline runs Claude to review Swift PRs for API compatibility breaks. The first run flags 12 issues with detailed reasoning. A developer fixes 3 issues and pushes a follow-up commit. The second pipeline run flags the same 9 remaining issues plus the same 3 the developer already fixed. What context injection prevents the re-flagging of already-fixed issues?

A) Inject the diff of the follow-up commit only, so Claude reviews only changed lines rather than the full file
B) Inject the list of previously flagged issues with their resolution status into the prompt context, so Claude knows which issues have been addressed
C) Cache the first run's output and skip the second run if fewer than 5 new files were changed
D) Increase `CLAUDE_CODE_MAX_OUTPUT_TOKENS` so Claude has room to reason about historical findings alongside new ones

<details><summary>Answer</summary>
**B)** Providing the resolution status of prior findings gives Claude the context to avoid re-flagging closed issues. This is the context-injection pattern for reducing repeat suggestions. A only reviewing the diff solves re-flagging of fixed lines but may miss issues that regressed in unchanged code or require whole-file context. C is wrong because skipping the review entirely would miss new issues in the unchanged files. D is wrong because output token count does not provide Claude with knowledge of previous findings. (source: Prompt engineering)
</details>

## Question 27
A CI pipeline posts Claude's review output directly to a PR comment via the GitHub API. A red team exercise shows that a malicious contributor could craft a commit message containing an HTML injection payload that gets embedded in Claude's output and rendered in the PR comment. What is the correct mitigation layer?

A) Add to the prompt: "Do not include content from commit messages verbatim in your output"
B) Enable HTML escaping on the GitHub API call by passing `mediaType: "raw"` instead of `mediaType: "html"` in the request
C) Sanitize Claude's output in the pipeline script — escape HTML entities before posting the string to the GitHub PR API
D) Switch from PR comments to a separate GitHub Check Run to isolate the output in a sandboxed UI element

<details><summary>Answer</summary>
**C)** Sanitizing output before posting to any external API is the correct pipeline-layer defense. Claude will naturally quote user-supplied content (commit messages) in its reviews; a prompt instruction cannot reliably prevent quoting. The pipeline must escape HTML entities before forwarding Claude's output to GitHub. A is wrong because "do not quote verbatim" would degrade review quality and Claude may still paraphrase in ways that include injected content. B is wrong because the `mediaType` parameter controls response format from the GitHub API, not input sanitization. D moves the problem to a different UI but does not sanitize the content. (source: Configuration and security)
</details>

## Question 28
A team wants to add Claude-powered review to their CI pipeline but is concerned about rate limiting during high-traffic periods when many developers push simultaneously. The pipeline currently makes synchronous requests. What architectural change best handles rate limit spikes without dropping reviews?

A) Implement exponential backoff with jitter in the pipeline: on a 429 response, wait and retry with increasing intervals up to a maximum retry count
B) Switch to the Message Batches API, which is not subject to rate limits because requests are queued server-side
C) Add a fixed 5-second sleep before each Claude API call to spread requests over time
D) Cache identical prompt+code combinations so repeated pushes of the same diff reuse the prior Claude response

<details><summary>Answer</summary>
**A)** Exponential backoff with jitter is the standard pattern for handling API rate limiting gracefully: it retries transient 429 errors without hammering the API, and jitter prevents thundering-herd re-collision. B is wrong because the Message Batches API is also subject to rate limits; it does not bypass them. C is wrong because a fixed sleep adds unnecessary latency during normal traffic and may still cause collisions during spikes. D is a valid cost optimization but does not handle rate limiting — identical diffs pushed simultaneously would still generate concurrent requests. (source: Configuration and security)
</details>

## Question 29
A Helm chart validation pipeline runs Claude to detect misconfigurations before deployment. The team wants to ensure that Claude has fresh knowledge of the company's internal Helm chart standards without changing the invocation command in every pipeline job. What is the cleanest configuration-as-code approach?

A) Create a `claude-standards.md` file and pass it via `--system-prompt claude-standards.md` in each pipeline job invocation
B) Place the Helm chart standards documentation in `CLAUDE.md` at the repository root so Claude Code automatically injects it as project context in every session
C) Store the standards in a GitHub Actions variable `CLAUDE_SYSTEM_CONTEXT` and reference it as `$CLAUDE_SYSTEM_CONTEXT` in the prompt string
D) Embed the standards as a comment block at the top of each Helm chart file so Claude reads them as part of the file context

<details><summary>Answer</summary>
**B)** `CLAUDE.md` is the designed mechanism for project-level context injection in Claude Code. It is loaded automatically without any flag changes to the invocation command, satisfying the "without changing the invocation command" requirement. Standards updates are just file edits, not pipeline script changes. A requires every pipeline job to include a `--system-prompt` flag, which is the opposite of "without changing the invocation command." C is wrong because `CLAUDE_SYSTEM_CONTEXT` is not a recognized Claude Code environment variable for system prompt injection. D embeds standards in source files, polluting the chart files with non-chart content and making standards updates require changes to every chart file. (source: Configuration and security)
</details>

## Question 30
A CI pipeline generates a nightly dependency vulnerability report for a Node.js monorepo with 120 packages. Each package gets one Claude analysis request. The report is delivered by email each morning and no developer is waiting synchronously. The team currently spends $180/month on this pipeline. Which change most directly reduces cost for this workload?

A) Reduce the number of packages scanned by filtering to only packages that changed in the last 7 days
B) Switch from the synchronous API to the Message Batches API; the nightly, non-blocking nature of the job makes it an ideal batch workload that delivers ~50% cost savings
C) Cache analysis results for packages whose lock file has not changed since the last nightly run and skip re-analysis for those packages
D) Downgrade from Claude Sonnet to Claude Haiku for all 120 package analyses to reduce per-request cost

<details><summary>Answer</summary>
**B)** The Message Batches API delivers ~50% cost reduction for exactly this pattern: 120 independent requests, nightly schedule, no synchronous consumer, latency-tolerant background job. At $180/month this saves approximately $90/month with no changes to the analysis quality or scope. A is a valid optimization but filtering to recently changed packages may miss vulnerabilities discovered in unchanged transitive dependencies. C is also a valid optimization that would reduce scope but requires maintaining cache state and may miss newly disclosed CVEs for unchanged packages. D reduces quality and may miss nuanced vulnerability analysis; it is a separate lever from the batch API cost optimization. (source: Message Batches API)
</details>
