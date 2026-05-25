# Module Bank: Developer Productivity with Claude

Auto-generated bank with 30 questions.

## Question 1
Your agentic code-review loop calls `fetch_diff`, `run_static_analysis`, and `query_issue_tracker` on every PR. You observe it alternating between `run_static_analysis` and `query_issue_tracker` indefinitely without ever calling `fetch_diff` or producing output. Each call returns valid data, but the loop never converges. What is the most precise diagnosis?

A) The `max_tokens` value is too low, causing the model to truncate its reasoning before reaching the `fetch_diff` call, which triggers a restart from the top of the tool list.
B) The loop has no semantic termination condition — it relies only on natural language in the model's output to decide when to stop, which never fires when the model stays in tool-calling mode.
C) The model is stuck because neither `run_static_analysis` nor `query_issue_tracker` produces output that changes the conversation state enough to shift the model's tool selection decision.
D) The issue tracker tool is returning paginated results; the model keeps re-querying the next page, which looks like spinning but is actually making progress through the dataset.

<details><summary>Answer</summary>
**C)** When consecutive tool calls return valid but non-progressing data, the model can get locked in a selection loop because its context never changes enough to shift its tool preference. The fix is to detect repeated identical tool call sequences (same tool, same arguments) and inject a state-change signal or escalate to a human. B) is partially right about missing termination but does not identify the specific mechanism causing the lock. A) is unrelated — truncation causes `stop_reason: "max_tokens"`, not looping. D) is a benign pattern distinguishable from spinning by checking whether arguments change across calls. (source: Agentic and multi-agent workflows)
</details>

## Question 2
You are designing a code-generation agent that writes a test file, runs `pytest`, reads the failure output, and fixes the implementation — repeating until all tests pass. A colleague argues for a hard cap of 10 iterations. You want a semantic termination condition instead. Which condition is most appropriate as the *primary* stop signal?

A) Stop when the model's response contains the phrase "all tests passing" anywhere in its text output.
B) Stop when `pytest` returns exit code 0 and the tool result confirms zero failures — a deterministic, externally-verified signal.
C) Stop when `stop_reason == "end_turn"` because that indicates the model has decided it is finished with the task.
D) Stop after the third consecutive identical `pytest` invocation on the same file, regardless of exit code.

<details><summary>Answer</summary>
**B)** A semantic stop condition should be grounded in an externally verifiable fact — `pytest` exit code 0 — not in natural language output (A) or model self-assessment (C). The test runner is the source of truth. `stop_reason == "end_turn"` (C) tells you the model stopped emitting tool calls, but it does not verify the task objective was met. An iteration cap and duplicate-call detection (D) serve as safety backstops, not primary conditions. (source: Agentic and multi-agent workflows)
</details>

## Question 3
An agentic refactoring loop has been running for 40 iterations. A developer reviewing the logs notices the agent has called `read_file("src/utils.py")` on iterations 3, 11, 22, and 38 with identical arguments and received the same content each time. The agent has also made real forward progress between those re-reads. Is this a problem?

A) Yes — any repeated tool call with identical arguments is a spinning indicator and must trigger an automatic loop abort regardless of whether other progress has been made.
B) No — re-reading a stable file multiple times during a long task is normal; the agent may need to refresh its working context for a file it partially processed earlier.
C) Yes — the agent should cache the file content after the first read and never call `read_file` again for the same path within a single session, treating redundancy as a bug.
D) No — but only if the re-reads happen at regular intervals; irregular re-read timing is the actual indicator of a stuck loop.

<details><summary>Answer</summary>
**B)** Distinguishing spinning from legitimate repetition requires checking whether the *overall loop* is making forward progress, not whether individual tool calls recur. Re-reading a shared utility file across a 40-iteration refactor is expected — the model may need to reconcile the file's current state at different points. A) is too broad; it would abort legitimate long-running tasks. C) would prevent the agent from detecting real file changes between its own edits. D) invents a timing-based heuristic with no basis in loop design documentation. (source: Agentic and multi-agent workflows)
</details>

## Question 4
Your deployment agent runs this sequence: `validate_config` → `provision_infra` → `deploy_app` → `run_smoke_tests`. It is implemented as a model-driven loop where the model selects each tool. In production, you discover the model occasionally skips `validate_config` when it "remembers" having validated the same config in a previous session. What is the correct architectural fix?

A) Increase the system prompt instructions to say "ALWAYS call validate_config first, no exceptions" and add the instruction in bold to emphasize priority.
B) Use `tool_choice: {"type": "tool", "name": "validate_config"}` for the first turn to programmatically force validation before handing control back to the model for subsequent steps.
C) Remove `validate_config` from the model's tool list and call it programmatically in the orchestrator before initiating the model-driven loop.
D) Both B and C are correct — the choice depends on whether validation requires model reasoning or is a pure infrastructure check.

<details><summary>Answer</summary>
**D)** Both approaches enforce the prerequisite deterministically. If `validate_config` requires the model to reason about the config content (e.g., detect semantic errors), forced `tool_choice` (B) keeps it in the model-driven flow while guaranteeing execution. If it is a pure programmatic check (e.g., schema validation), calling it outside the loop (C) is cleaner and removes the model from the critical path. A) relies on the model following instructions — the documented anti-pattern for safety-critical prerequisites. (source: Agentic and multi-agent workflows)
</details>

## Question 5
A developer implements loop resumption after human interruption: when a developer pauses the agent mid-task, approves a plan change, and resumes, the agent starts from the beginning because none of the completed work is preserved. What state should the loop persist to enable mid-task resumption?

A) Only the final assistant message from before the pause, so the model can regenerate the full plan from that checkpoint without needing the intermediate tool call history.
B) The complete conversation history including all tool calls, tool results, assistant reasoning, and the current iteration counter, so the model resumes with full context of what it has already done.
C) The list of completed tool names and their arguments only — the actual results can be discarded to save storage because the model can re-derive them from the tool arguments.
D) A natural-language summary of completed steps generated by the model at pause time, which is smaller than the full history and sufficient for the model to reconstruct its working state.

<details><summary>Answer</summary>
**B)** Resumption requires full conversation history — tool calls, tool results, and assistant reasoning — because the model's next decision depends on what it has already learned. The iteration counter is needed for safety cap enforcement. A) loses tool result data needed for reasoning. C) discards results that the model cannot always re-derive and that may have changed (e.g., file contents). D) introduces lossy compression; a summary omits specific values (file paths, line numbers, error messages) the model needs to continue precisely. (source: Agentic and multi-agent workflows)
</details>

## Question 6
You are building a CI pipeline where `claude -p` analyzes test failure logs and outputs a JSON object with a `root_cause` and `suggested_fix` field. On 15% of runs the agent enters a research loop — calling `search_docs` and `read_file` repeatedly — and never emits the final JSON, causing a pipeline timeout. The model never returns `stop_reason: "max_tokens"`. What is the most likely cause and fix?

A) The model's extended thinking budget is exhausted mid-loop; increase `budget_tokens` from the default 1024 to 10000 to give it enough reasoning space to converge.
B) The model lacks a clear output signal — add an explicit instruction in the prompt: "Once you have enough information, stop calling tools and emit only the JSON object on a single line."
C) The `stop_reason` field is missing in the response because the `--output-format json` flag suppresses it; switch to `--output-format text` to restore proper loop termination signals.
D) The search and read tools are returning too much data per call, flooding the context window; truncate tool outputs to 500 tokens per response to force faster convergence.

<details><summary>Answer</summary>
**B)** When the model has no explicit instruction to switch from information-gathering mode to output mode, it can continue calling tools indefinitely — especially when each call returns potentially relevant new data. Adding a clear trigger ("once you have enough information, stop and emit JSON") gives the model a behavioral anchor to transition states. A) conflates extended thinking budget with loop convergence — the issue is a missing output trigger, not reasoning depth. C) `--output-format json` does not suppress `stop_reason` in the underlying API response. D) truncating tool outputs is a useful secondary measure but does not address the missing convergence instruction. (source: Agentic and multi-agent workflows)
</details>

## Question 7
An MCP tool called `update_ticket` has this description: "Updates a ticket." In production, the agent calls it with `status`, `assignee`, and `priority` all set in the same call when it should be setting only `status`. What description change best prevents over-parameterization?

A) Add a warning: "Do not pass more than one field at a time to this tool."
B) Rewrite to specify each parameter's purpose, when to omit it, and provide a minimal example: "Updates one or more fields of an existing ticket. Pass only the fields you intend to change — omitting a field leaves it unchanged. E.g., `{\"ticket_id\": \"T-42\", \"status\": \"closed\"}` closes ticket T-42 without touching assignee or priority."
C) Split into three tools: `set_ticket_status`, `set_ticket_assignee`, and `set_ticket_priority` with one-field-per-tool descriptions.
D) Add JSON schema `maxProperties: 2` to limit the number of fields the model can pass per call.

<details><summary>Answer</summary>
**B)** The root cause is that the description gives the model no guidance on when to include or omit each field. Rewriting with a concrete minimal example — showing a single-field update — teaches the model that partial updates are the normal pattern. C) solves the over-parameterization but creates fragmentation; three round trips to change all three fields is worse than one. A) is a negative constraint without positive guidance; the model may still pass all fields if it does not understand partial-update semantics. D) restricts `ticket_id` + one field max, which incorrectly prevents legitimate multi-field updates. (source: MCP documentation)
</details>

## Question 8
You are designing a documentation assistant MCP server. A product manager asks you to create a single `search_docs` tool that accepts a `mode` parameter with values `"semantic"`, `"keyword"`, and `"title_exact"` to unify three different search backends. What is the primary risk of this design?

A) Having a `mode` parameter prevents the MCP server from caching results because the cache key would need to include the mode value, tripling storage requirements.
B) The model must reason about which mode to pass on every call, reintroducing the same selection problem that separate tool names would have solved at the routing level.
C) MCP servers do not support enum-constrained parameters; the `mode` field would need to be a free-text string, making validation impossible server-side.
D) The unified tool will always default to `"semantic"` mode because LLMs prefer semantic search, making `"keyword"` and `"title_exact"` modes unreachable in practice.

<details><summary>Answer</summary>
**B)** Merging semantically distinct operations behind a `mode` parameter moves the selection decision from tool routing (where tool names provide a clear signal) to parameter interpretation (where the model must reason about an enum value). This is the same ambiguity problem as having poorly named tools, just pushed one level deeper. A) is a fabricated performance concern. C) MCP tools do support enum-constrained parameters via JSON Schema. D) is an overgeneralization — mode selection depends on the prompt and context, not a fixed preference. (source: MCP documentation)
</details>

## Question 9
Your MCP server's `run_query` tool returns the full raw SQL result set as a JSON array, sometimes with 2,000+ rows. The agent's context window fills quickly, degrading performance on long sessions. Where is the best place to address this?

A) Add a `PostToolUse` hook that detects large tool results and summarizes them with a secondary model call before injecting them into the conversation.
B) Truncate or paginate the tool result at the MCP server level — return at most 50 rows plus a `has_more` field and a cursor for subsequent pages.
C) Increase the context window by switching to claude-opus-4 which supports a larger token limit, giving the agent more headroom before degradation occurs.
D) Instruct the model in the system prompt to ignore rows beyond the first 50 and treat large results as if they were truncated automatically.

<details><summary>Answer</summary>
**B)** Tool result verbosity should be controlled at the source — the MCP server. Returning paginated results with a cursor keeps individual tool results small, lets the agent fetch only what it needs, and avoids filling the context with unneeded data. A) adds latency and token cost for every large result, even when the agent only needed the first few rows. C) is a scaling workaround, not a fix — the root cause is unbounded output. D) relies on the model following a truncation instruction, which is probabilistic and wastes tokens even on "ignored" rows. (source: MCP documentation)
</details>

## Question 10
A junior developer asks whether their `file_writer` MCP tool should validate that the `path` parameter does not contain `..` segments before writing. They argue: "The model is smart enough not to send path traversal attacks to itself." What is the correct position?

A) Agree — LLMs have internal safety filtering that prevents them from constructing malicious paths, making server-side path validation redundant.
B) Validate at the tool boundary regardless of trust in the model — tools are callable by any agent, script, or future integration, and defense-in-depth requires validation that does not depend on the caller's good behavior.
C) Move path validation into a `PreToolUse` hook instead of the server, so validation logic can be updated without redeploying the MCP server.
D) Validate only in production environments; skip validation in development to reduce friction during local testing.

<details><summary>Answer</summary>
**B)** Tool boundary validation is a defense-in-depth principle: the server should not trust its callers, including models. A model can be prompt-injected, misled by a malicious tool result, or replaced by a different caller in future integrations. Validating at the server makes the tool safe regardless of caller. A) is false — models do not have reliable internal path traversal filtering. C) hooks are a valid additional layer but should not be the *only* layer; the MCP server itself must validate its own preconditions. D) removes protection during the development phase where accidental misuse is most likely. (source: MCP documentation)
</details>

## Question 11
Your team is choosing transport for a new MCP server that will be embedded inside each developer's IDE plugin, running on the same machine as Claude Code, with no network access required. Which transport is appropriate and why?

A) HTTP with SSE — it is the standard for production MCP deployments and provides connection resilience that stdio lacks.
B) stdio — it is the correct transport for local, single-process, same-machine communication; no networking stack is needed and it has lower overhead.
C) WebSocket — it supports bidirectional streaming which is required for long-running tool calls that need to push progress updates back to the client.
D) HTTP with SSE for tool calls and stdio for server initialization, because MCP requires a hybrid transport for IDE integrations.

<details><summary>Answer</summary>
**B)** stdio is the documented transport for local MCP servers running on the same machine as the client. It requires no network configuration, has minimal overhead, and is the standard for IDE plugin integrations. HTTP/SSE (A) is designed for remote or multi-client MCP servers where network transport is required. C) WebSocket is not a standard MCP transport. D) describes a non-existent hybrid mode. (source: MCP documentation)
</details>

## Question 12
You have a `code_review` MCP tool whose description is 800 characters and includes inline examples of correct usage. A colleague flags it as "too long" and wants to trim it to under 100 characters for performance. What is the correct position?

A) Agree — tool descriptions above 200 characters have documented performance degradation on tool selection accuracy in Claude models.
B) Disagree — description length should be driven by the minimum needed for unambiguous correct use; if 800 characters removes selection errors, that length is justified.
C) Agree — move the inline examples from the description into the parameter-level JSON schema descriptions instead, which are not subject to the same length limits.
D) Disagree only if the tool is the only one in the set; with multiple tools, shorter descriptions are mandatory to keep total tool definition tokens under 4096.

<details><summary>Answer</summary>
**B)** There is no documented character limit that triggers accuracy degradation in Claude. Description quality — specificity, examples, disambiguation — is what matters. If 800 characters is what it takes to reliably distinguish the tool's use case from alternatives, that length is correct. A) and D) cite non-existent limits. C) is a reasonable organization strategy but not a response to a false performance concern — the real issue is whether the description serves model comprehension. (source: MCP documentation)
</details>

## Question 13
You are building an API that generates and caches architecture documentation for a large monorepo. Each call to the endpoint passes the 4,000-token architecture doc as part of the system prompt, followed by a developer's specific question. Across 500 daily calls, the architecture doc never changes. What is the most effective cost-reduction pattern?

A) Store the architecture doc in a vector database, retrieve only the top-3 relevant sections per call, and inject them instead of the full doc to reduce per-call token count.
B) Apply `cache_control: {type: "ephemeral"}` to the architecture doc content block in the system prompt so it is cached server-side and subsequent calls within the TTL pay only for the cache read, not re-processing.
C) Compress the architecture doc to 1,000 tokens using an extractive summarization step run nightly, trading coverage for lower cost.
D) Use a single long-running conversation session with all 500 developers sharing one session context, amortizing the architecture doc tokens across all calls in the session.

<details><summary>Answer</summary>
**B)** Prompt caching with `cache_control: {type: "ephemeral"}` is the Claude-native pattern for this exact scenario: stable, repeated context at the start of a prompt. It caches the architecture doc tokens server-side, reducing each subsequent call's cost to the cache-read price. A) is a valid RAG approach but discards cross-section relationships and adds retrieval infrastructure. C) degrades accuracy for cost savings that prompt caching achieves without information loss. D) sharing a session across 500 developers is architecturally unsound and violates session isolation. (source: Extended thinking / Prompt caching)
</details>

## Question 14
A developer is using the Anthropic API with `thinking: {type: "enabled", budget_tokens: 16000}` to design a microservices decomposition for a 200k-line monolith. The model returns a high-quality response. A colleague then enables the same thinking config for a tool that simply formats a date string from ISO 8601 to `MM/DD/YYYY`. What is wrong with the second use?

A) Extended thinking cannot be used alongside tool definitions in the same API call, so enabling it on a formatting tool will silently disable the model's tool-calling capability.
B) 16000 `budget_tokens` is significant compute cost allocated to a deterministic, trivial transformation that requires no chain-of-thought reasoning — the budget is wasted.
C) Extended thinking for date formatting will cause the model to second-guess the ISO 8601 format and introduce timezone conversion errors it would not make without thinking enabled.
D) The extended thinking budget applies globally across all tools in the session, so enabling it on the formatting tool steals budget from other more complex tools in the same call.

<details><summary>Answer</summary>
**B)** Extended thinking is valuable for problems requiring multi-step reasoning, trade-off analysis, or planning. A date format conversion is a deterministic transformation — allocating 16000 thinking tokens to it wastes compute with no quality benefit. A) is false — extended thinking works alongside tool use. C) thinking does not introduce transformation errors; it is additive reasoning, not noise injection. D) `budget_tokens` is a per-call ceiling, not a shared pool across tools — each call has its own budget. (source: Extended thinking)
</details>

## Question 15
Your team runs a weekly architecture review using Claude. Each session starts with a developer pasting 6,000 tokens of codebase context, then asking 10-15 questions over the course of 90 minutes. By question 12, response quality has degraded and the model starts contradicting its earlier answers. What is the most likely cause and best mitigation?

A) The 90-minute session duration triggers a rate-limit that degrades response quality; split sessions to stay under 60 minutes each.
B) Accumulated conversation history has pushed the total context near the context window limit, causing older architectural context to fall out of the active window. Summarize the conversation state mid-session and start a fresh turn with the summary plus the original codebase context.
C) The model's internal state drifts over long sessions due to numerical precision issues in the attention mechanism; switching to a different model instance resets this drift.
D) The developer is asking questions too quickly; add a 30-second delay between questions to allow the model's internal cache to settle.

<details><summary>Answer</summary>
**B)** As conversation history grows, total context length approaches the window limit. When the model's context is truncated or compressed, earlier architectural context gets displaced, leading to contradictions and degraded coherence. The correct mitigation is a mid-session summarization checkpoint: ask the model to summarize agreed-upon architecture decisions, then start a new turn with that summary plus the original codebase context. A) invents a rate-limit quality degradation that does not exist. C) is technically unfounded. D) response cache settling is not a real mechanism. (source: Agentic and multi-agent workflows)
</details>

## Question 16
A developer uses Claude Code to do a code review on the same feature branch they have been implementing for the past 3 hours in the same session. They notice Claude Code consistently rates their code quality highly and misses structural issues that a colleague later catches easily. What is the most likely explanation?

A) Claude Code's code review quality degrades after 3 hours due to session token limits approaching maximum capacity.
B) The model has developed confirmation bias from hours of helping build the feature — it has "seen" the author's intent and rationale in context, making it less likely to question structural choices it helped make.
C) Claude Code uses a cached code quality score from the initial architecture discussion and does not re-evaluate from scratch when reviewing the same files later.
D) The colleague who caught the issues has a higher-tier Claude subscription with access to a more capable review model.

<details><summary>Answer</summary>
**B)** When the same Claude Code session that built the code performs the review, the model has extensive context about the author's reasoning, design intent, and constraints. This context biases the review toward leniency — the model implicitly understands "why" decisions were made and is less likely to flag them as problematic. The documented fix is to perform code review in a fresh session with only the diff as context, eliminating accumulated author-intent bias. A) is a secondary effect but does not explain the directional bias toward positive ratings. C) describes a non-existent score caching mechanism. D) is irrelevant. (source: Developer workflow)
</details>

## Question 17
You are automating refactoring of a 10,000-line Python service to replace all uses of a deprecated `requests` library with `httpx`. Before running the automated refactor, which safety check is most critical?

A) Confirm the `httpx` package version is pinned in `requirements.txt` and that its API is fully backward-compatible with `requests` for all usage patterns present in the codebase.
B) Run `mypy` on the current codebase to establish a type-error baseline so you can distinguish pre-existing errors from refactor-introduced regressions in the post-refactor check.
C) Verify that a comprehensive test suite exists and is currently passing before the refactor begins, so test failures after the refactor can be attributed to the change rather than pre-existing breakage.
D) Use `git log --all -- "*.py"` to identify which team members last touched each file, so you can notify them before the refactor runs on their files.

<details><summary>Answer</summary>
**C)** The most critical pre-refactor safety check is confirming the test suite is green before touching anything. Without a passing baseline, you cannot distinguish regressions caused by the refactor from pre-existing failures. A) is important but secondary — API compatibility analysis tells you what *might* break, while tests tell you what *does* break. B) is a useful secondary check for typed codebases but covers only type errors, not behavioral regressions. D) is a team process concern, not a technical safety check. (source: Developer workflow)
</details>

## Question 18
A developer asks Claude Code to generate tests for a 200-line `PaymentProcessor` class as part of a refactoring workflow. Claude Code generates 15 unit tests. The developer approves them. What should happen before the refactoring edits begin?

A) Run the newly generated tests immediately to establish a passing baseline — tests that fail before the refactor indicate either test generation errors or bugs in the existing code, both of which must be resolved first.
B) Commit the tests to a separate branch and open a PR for team review before running them, since unreviewed tests may encode incorrect assumptions that get locked in as baseline.
C) Proceed directly to refactoring — the tests are the specification, so they will fail initially and the refactor's goal is to make them pass.
D) Delete any tests that rely on private methods because those will break after the refactor changes internal implementation details.

<details><summary>Answer</summary>
**A)** Tests generated before a refactor must pass against the *existing* code first. If they fail on the current implementation, they either contain errors or expose pre-existing bugs — either way, proceeding to refactor against broken tests produces an unreliable safety net. B) adds process overhead that delays the refactor without improving safety over a simple local run. C) inverts the workflow — tests for *existing behavior* should pass before a refactor, not after. D) discards coverage without investigation; a generated test on a private method via its public interface is valid. (source: Developer workflow)
</details>

## Question 19
A developer is reviewing a 3,000-line PR using Claude Code. They paste the full diff in a single prompt. Claude Code returns a high-level review that misses several subtle logic errors in individual functions. What technique most improves review depth on large PRs?

A) Ask for the review twice in the same session and average the findings, since two passes cover different aspects of the diff.
B) Break the PR into logical file-group chunks — e.g., data model changes, business logic changes, API layer changes — and review each chunk in a separate focused prompt, then synthesize findings.
C) Switch to extended thinking with a large `budget_tokens` value so the model performs deep multi-step reasoning over the full 3,000-line diff in a single pass.
D) Add "be thorough and check every function for logic errors" to the review prompt to redirect the model's attention to function-level detail.

<details><summary>Answer</summary>
**B)** Breaking a large diff into semantically coherent chunks and reviewing each in a focused prompt concentrates the model's attention on a manageable scope per review, dramatically improving the depth of analysis within each chunk. A) two passes improve breadth by chance but do not guarantee depth on any specific area. C) extended thinking helps with complex reasoning but a 3,000-line diff still exhausts attention breadth even with deep thinking enabled — chunking is complementary and more effective. D) instruction prompting for thoroughness has diminishing returns against a context-window attention problem. (source: Developer workflow)
</details>

## Question 20
A team wants to use a `git commit-msg` hook that calls `claude -p` to rewrite commit messages to conform to Conventional Commits format (e.g., `feat:`, `fix:`, `chore:`). The hook must complete within 3 seconds to avoid frustrating developers. What design choice most impacts latency?

A) Use the `claude-haiku-4` model instead of `claude-sonnet-4-5` — the smaller model produces commit message reformatting in under 1 second while the larger model averages 4-6 seconds for the same task.
B) Apply prompt caching to the Conventional Commits specification block in the system prompt, which is sent on every hook invocation and never changes between commits.
C) Run the hook asynchronously in the background and have the developer manually copy the rewritten message from a temp file after the `git commit` completes.
D) Reduce the system prompt to a single sentence and pass only the first line of the commit message, discarding the message body to minimize input tokens.

<details><summary>Answer</summary>
**B)** The Conventional Commits specification is a stable, repeated system prompt block. Applying `cache_control: {type: "ephemeral"}` means the specification tokens are cached after the first invocation, reducing per-hook TTFB significantly. A) is also effective for latency but trades output quality; caching is a complementary technique that improves latency without downgrading the model. C) breaks the synchronous nature of `commit-msg` hooks — the commit has already been created before the developer can apply the rewritten message. D) discarding the message body removes context needed for accurate categorization (e.g., distinguishing a `feat` from a `fix`). (source: Prompt caching / Developer workflow)
</details>

## Question 21
A developer is mid-session with Claude Code after 45 minutes of building a React component. They now want Claude Code to perform a critical security review of the authentication module — an unrelated file they have not touched in this session. Should they start a new session or continue?

A) Continue in the same session — the longer context gives Claude Code more background about the codebase architecture, which improves security review quality even for unrelated files.
B) Start a new session for the security review — fresh context eliminates accumulated bias from the UI development work and focuses attention entirely on the authentication module.
C) Continue, but first ask Claude Code to summarize the session so far and output it as a CLAUDE.md snippet, which will carry over to the new session automatically.
D) It makes no practical difference — Claude Code's security review quality is determined by the model version, not session context.

<details><summary>Answer</summary>
**B)** A fresh session for a critical security review is the correct pattern. The 45-minute context of UI component work is irrelevant to authentication security and creates noise. More importantly, the security review should be conducted without the developer's implementation context biasing the model toward leniency. A) overstates the value of unrelated context; accumulated UI-building context does not improve security analysis. C) CLAUDE.md snippets are not automatically carried over to new sessions without explicit configuration. D) context does materially affect review quality and bias. (source: Developer workflow)
</details>

## Question 22
You are setting up `claude` as a background daemon in a Docker container. The container starts successfully, but `claude` exits immediately with exit code 2. No API errors appear in the logs. What does exit code 2 indicate and what should you check first?

A) Exit code 2 means an API authentication failure — verify `ANTHROPIC_API_KEY` is set and valid in the container environment.
B) Exit code 2 indicates a usage error — a missing required argument, an unrecognized flag, or an invalid combination of options in the command invocation.
C) Exit code 2 is a network timeout code returned when the container cannot reach the Anthropic API endpoint within 10 seconds of startup.
D) Exit code 2 means the Claude Code binary detected it is running as root inside a container and refuses to execute for security reasons.

<details><summary>Answer</summary>
**B)** In Unix convention, exit code 2 typically signals a usage error — an invalid flag, missing required argument, or incompatible option combination. Before checking API credentials or network, review the exact `claude` invocation for argument errors. A) API authentication failures return a different exit code (typically 1 with an error message to stderr). C) invents a timeout-specific code assignment. D) describes a non-existent root-detection security block in Claude Code. (source: Developer workflow / CLI)
</details>

## Question 23
You are debugging why Claude Code made an incorrect edit: it replaced `user.account_id` with `user.id` throughout a service, breaking a feature that relies on `account_id` being a separate field. You review the session. Claude Code had access to the correct schema file but never read it during the session. What is the root cause?

A) Claude Code has a known bug where it skips schema file reads when the filename contains an underscore — rename the file to `schema.json` to trigger automatic discovery.
B) The schema file was never explicitly provided to or read by Claude Code in the session; the model made the substitution based on general knowledge of common ID field naming conventions rather than the actual schema.
C) Extended thinking was not enabled; without it, Claude Code cannot reason about field relationships across multiple files and defaults to common naming patterns.
D) The system prompt did not include a `read_schema_first` instruction; Claude Code only reads schema files when explicitly instructed to do so via system prompt directives.

<details><summary>Answer</summary>
**B)** Claude Code builds context from what it has explicitly read in the session. If the schema file was available but never read, the model had no ground truth about the field definitions and fell back on training-data intuition (`user.id` is a common pattern). The fix is to either explicitly ask Claude Code to read the schema before making field-related changes or ensure the relevant files are in the initial context. A) describes a non-existent filename restriction. C) extended thinking is unrelated to file reading. D) Claude Code reads files proactively in many contexts — the root cause is not a missing instruction. (source: Reliability and debugging)
</details>

## Question 24
A developer's agentic task fails and they want to retry. The original prompt was: "Refactor the auth module to use async/await." The model made syntactically valid changes but introduced a logic error in the token refresh flow. Should they retry with the same prompt or reformulate?

A) Retry with the same prompt — the model's outputs are stochastic and a re-run may produce a correct implementation by chance.
B) Reformulate — add the specific constraint that failed: "Refactor the auth module to use async/await. Preserve the token refresh logic exactly: the refresh must be called exactly once per expired token, blocking other requests until it completes."
C) Retry with the same prompt but switch to a larger model to reduce the probability of logic errors.
D) Retry the same prompt but add "be careful with the token refresh flow" as a general caution at the end.

<details><summary>Answer</summary>
**B)** When an agentic task fails due to a specific, identifiable constraint violation, the correct response is to reformulate the prompt with that constraint made explicit. The original prompt did not specify the token refresh semantics — the model had no way to preserve them correctly. Retrying the same prompt (A, C) without adding the missing constraint will reproduce the same class of error. D) is a vague caution that does not encode the actual constraint. (source: Reliability and debugging)
</details>

## Question 25
You are building observability for a multi-step agentic code review pipeline. A colleague argues you only need to log the final output. You want more. Which set of log events provides the minimum necessary signal for diagnosing production failures?

A) Log only `stop_reason` values per turn and the final assistant message — this captures termination behavior and output without storing sensitive intermediate data.
B) Log each tool call with its name, arguments (sanitized), result, timestamp, and the `stop_reason` for each turn — this gives a complete execution trace showing exactly where the loop diverged from expected behavior.
C) Log only tool call failures — successful tool calls produce no diagnostic value and logging them adds storage cost without improving debuggability.
D) Log the first and last assistant messages per session — the intermediate steps are implementation details that should not be stored for compliance reasons.

<details><summary>Answer</summary>
**B)** A complete execution trace — tool calls, arguments, results, and `stop_reason` per turn — is the minimum necessary to diagnose failures. Without intermediate tool calls, you cannot determine which step failed, what arguments triggered the error, or where the loop went off track. A) loses the tool call trace needed for root cause analysis. C) successful tool calls are needed to understand what the model "knew" at each step before a failure. D) intermediate steps are the diagnostic content; logging only endpoints is insufficient. (source: Reliability and debugging)
</details>

## Question 26
An agentic workflow has been running correctly for weeks. On Monday morning, 80% of runs fail with `ToolExecutionError: resource not found` from the `fetch_pr_metadata` tool. The prompt, code, and model version are unchanged. What should you investigate first?

A) Check whether an API version deprecation was announced — Anthropic may have changed the tool calling protocol over the weekend.
B) Investigate the external dependency: the tool calls an external PR API that may have changed its endpoint URL, authentication scheme, or response schema since Friday.
C) Check the `budget_tokens` parameter — a weekend configuration push may have reduced the thinking budget below the threshold needed for the tool to execute correctly.
D) Re-run the same tasks with extended thinking enabled to get deeper reasoning about why the tool is failing before investigating the infrastructure.

<details><summary>Answer</summary>
**B)** When an agentic workflow that was stable fails suddenly without any code changes, the most likely cause is an external dependency change: an API endpoint moved, an auth token expired, a rate limit changed, or a response schema was updated. These changes happen on provider timelines, not yours. A) Anthropic API protocol changes are versioned and announced well in advance. C) `budget_tokens` changes do not cause `resource not found` errors. D) extended thinking investigates the reasoning chain, not infrastructure failures. (source: Reliability and debugging)
</details>

## Question 27
A developer on your team reports that their `claude` sessions consistently produce lower-quality outputs than their colleague's for the same tasks. Both are using the same model, same prompts, and same project. After investigation, you find the developer's `~/.claude/settings.json` has `"maxTokens": 512`. What is the effect and fix?

A) `maxTokens: 512` limits how many tokens the model receives as input — increase it to at least 8192 to allow full prompts to be processed by the model.
B) `maxTokens: 512` caps the model's output at 512 tokens per turn, causing truncated responses. The developer should increase or remove this limit to allow full-length responses.
C) `maxTokens: 512` has no effect on output quality but reduces billing cost by stopping the model early — it is a legitimate cost-saving measure without quality trade-offs.
D) `maxTokens: 512` limits the number of tool calls per session, not response length, so quality issues must have a different root cause.

<details><summary>Answer</summary>
**B)** `maxTokens` (or `max_tokens`) controls the output token limit. At 512 tokens, any response requiring more than that — detailed code reviews, multi-file analysis, long implementations — gets truncated mid-output. The model appears to give incomplete or superficial answers. Removing the cap or setting it to a value appropriate for the task (e.g., 4096+) restores full response quality. A) inverts the parameter's direction — it controls output, not input. C) truncation at 512 tokens causes quality degradation, not just cost savings. D) misidentifies what `maxTokens` controls. (source: CLI / Developer workflow)
</details>

## Question 28
You want Claude Code to automatically open the relevant Jira ticket in a browser whenever it reads a file that contains a `# JIRA: PROJ-XXXX` comment. Which mechanism implements this correctly?

A) Add a `PostToolUse` hook matching `tool_name: "Read"` that scans the tool result for the `# JIRA:` pattern and, when found, uses `xdg-open` or `open` to launch the browser with the ticket URL.
B) Add a `UserPromptSubmit` hook that searches all staged files for Jira references before every prompt and pre-opens all referenced tickets proactively at session start.
C) Add a `PreToolUse` hook matching `tool_name: "Read"` that reads the file in the hook, extracts the Jira reference, opens the browser, and then allows the `Read` tool to proceed normally.
D) Add a `Stop` hook that scans all files read during the session and batch-opens Jira tickets for everything encountered, so browser tabs are opened at session end rather than per-read.

<details><summary>Answer</summary>
**A)** `PostToolUse` fires after `Read` completes and has access to the file content in the tool result — the correct place to scan for Jira references and trigger a side effect. B) scans files before they are read and opens all tickets upfront, which is noisy and doesn't match the "when Claude reads a file" trigger. C) `PreToolUse` fires before the file is read, so the hook cannot inspect file content — it would need to independently re-read the file, causing duplicate I/O and a race condition. D) defers the action to session end, far too late to be useful during active development. (source: CLI / Developer workflow)
</details>

## Question 29
A team uses `claude -p` to generate release notes from a CHANGELOG diff as the last step in their release pipeline. Occasionally the pipeline passes but the generated release notes are empty strings. The model does not error. What should you add to detect this silently failing case?

A) Add `--verbose` to the `claude -p` invocation to see the model's internal reasoning, which will reveal why it produced an empty response on those runs.
B) After the `claude -p` call, check that `jq '.result'` returns a non-empty string and exit non-zero if empty, treating empty output as a pipeline failure regardless of CLI exit code.
C) Switch to `--output-format stream-json` and detect the `content_block_stop` event, which is omitted when the model produces empty output, signaling a generation failure.
D) Add a `PostToolUse` hook that monitors the model's output buffer and alerts when fewer than 100 tokens are produced for a release notes generation task.

<details><summary>Answer</summary>
**B)** `claude -p` exits 0 on successful model calls regardless of whether the output is meaningful. The correct pattern is to validate the output content in the calling script: parse the JSON response, extract `.result`, and treat an empty or whitespace-only string as a pipeline failure by exiting non-zero. A) `--verbose` shows CLI metadata, not the model's reasoning about why it generated nothing. C) `content_block_stop` is emitted for every content block including empty ones — its presence does not signal non-empty content. D) hooks cannot monitor output buffer token counts; `PostToolUse` monitors tool results, not model generation. (source: CLI / Reliability and debugging)
</details>

## Question 30
A developer pair-programming with Claude Code asks it to "add input validation to the checkout form." Claude Code makes six edits across four files. The developer reviews two of the edits, approves them, and asks Claude Code to continue with unrelated database work. Later, a colleague's review finds that the other four validation edits introduced a regression. What workflow practice would have prevented this?

A) Always use `--dangerously-skip-permissions` during pair programming to allow Claude Code to complete all related edits atomically without interruption.
B) Before pivoting to the next task, run the test suite and review all edits from the previous task — only continue when the batch of changes is confirmed correct and tests pass.
C) Limit Claude Code to one file edit per turn to reduce the number of changes that need reviewing before a pivot to a new task.
D) Ask Claude Code to write a summary of its edits in a CHANGES.md file after each task so the developer can review the summary instead of individual file diffs.

<details><summary>Answer</summary>
**B)** The regression occurred because the developer reviewed only part of a multi-file change set before pivoting. The correct practice is to complete the review cycle — run tests and review all edits — before starting an unrelated task. This creates a clean checkpoint and ensures the codebase is in a known-good state before new changes compound on top of unreviewed ones. A) bypassing permissions makes the problem worse by encouraging unchecked edits. C) limits productivity; a one-edit-per-turn constraint is not a substitute for proper review. D) a summary file is not a substitute for reviewing and testing the actual changes. (source: Developer workflow)
</details>
