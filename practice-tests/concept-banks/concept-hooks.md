# Hooks & Workflow Control — Question Bank

## Question 1
You need to ensure formatting always runs after file edits, regardless of model behavior. Best hook pattern?

A) `UserPromptSubmit` with prompt reminder
B) `PostToolUse` matcher `Edit|Write` + formatter command
C) `Stop` hook with manual checklist
D) `Notification` hook

<details>
<summary>Answer</summary>

**B)** PostToolUse with a matcher targeting Edit and Write fires a deterministic command hook every time either tool completes, guaranteeing the formatter runs regardless of what the model decides to do next. A is wrong because UserPromptSubmit fires before Claude sees the user message, not after a file edit, so it cannot guarantee post-edit formatting and relies on the model complying with a prompt reminder. C is wrong because Stop fires at turn end, not after each individual file edit, so multiple edits in one turn would only trigger one formatter run at the end. D is wrong because Notification fires when Claude sends a notification (idle prompts, permission prompts), which is unrelated to file edit events. (source: Hooks guide)

</details>

---

## Question 2
A teammate asks what stream command hooks read input from. Correct answer?

A) `stdout`
B) `stderr`
C) `stdin`
D) HTTP response body

<details>
<summary>Answer</summary>

**C)** Command hooks receive their input payload (the hook context JSON) on stdin, allowing the shell script or binary to read tool name, arguments, and other event data from standard input. A is wrong because stdout is how a command hook sends its response back to Claude Code, not how it receives input. B is wrong because stderr is used for error output from the hook process and is not the input channel. D is wrong because HTTP response body is the response mechanism for http-type hooks, not for command-type hooks. (source: Hooks guide)

</details>

---

## Question 3
You want to deny destructive Bash commands before execution. Best event?

A) `PostToolUse`
B) `PreToolUse`
C) `Stop`
D) `SessionEnd`

<details>
<summary>Answer</summary>

**B)** PreToolUse fires before the tool executes, giving the hook a chance to return a permissionDecision of deny to block the command entirely before any harm is done. A is wrong because PostToolUse fires after the tool has already executed, so by the time the hook runs the destructive command has already completed and cannot be undone. C is wrong because Stop fires at the end of a turn after all tool calls have already run, making it too late to block any specific tool execution. D is wrong because SessionEnd fires when the session is ending, which is far too late to intercept individual tool calls during the session. (source: Hooks guide)

</details>

---

## Question 4
Why use `matcher: "Bash"` and `if: "Bash(rm *)"` together?

A) Required by JSON parser
B) `matcher` is regex only, `if` is exact only
C) Coarse filter first, precise argument-level filter second
D) `if` replaces `matcher`

<details>
<summary>Answer</summary>

**C)** The matcher field performs a fast, coarse filter on the tool name so the hook only loads for Bash events at all, while the if field performs a precise argument-level check that can inspect the full command string including parameters like "rm *". This two-stage approach reduces unnecessary hook invocations while providing fine-grained control. A is wrong because there is no JSON parser requirement driving this pattern — both fields are optional and independent. B is wrong because both fields support pattern matching; the distinction is not regex-vs-exact but rather tool-name scope vs. full-command expression scope. D is wrong because if does not replace matcher; matcher scopes which events load the hook at all, while if acts as an additional condition within those events. (source: Hooks guide)

</details>

---

## Question 5
You need to auto-approve only `ExitPlanMode` permission prompts. Which event?

A) `PermissionRequest`
B) `PermissionDenied`
C) `UserPromptExpansion`
D) `StopFailure`

<details>
<summary>Answer</summary>

**A)** PermissionRequest fires when Claude Code is about to display a permission prompt, and a hook can return a permissionDecision of allow with a matcher filtering for ExitPlanMode to auto-approve only that specific prompt type. B is wrong because PermissionDenied fires after a permission has already been denied and can signal retry, but cannot intercept and pre-approve a pending permission request. C is wrong because UserPromptExpansion fires when a user slash command is expanded into a prompt before Claude sees it, which is unrelated to permission prompt interception. D is wrong because StopFailure fires when a turn ends due to an API or execution error, not when a permission prompt is raised. (source: Hooks guide)

</details>

---

## Question 6
You changed `.envrc` and want Claude environment refreshed automatically. Best hook setup?

A) `SessionEnd` only
B) `CwdChanged` only
C) `SessionStart` + `CwdChanged` (+ optional `FileChanged` watch)
D) `PostCompact`

<details>
<summary>Answer</summary>

**C)** SessionStart ensures the environment is loaded fresh at the beginning of every session, CwdChanged reloads it whenever the working directory changes (which may load a different .envrc), and an optional FileChanged watcher on .envrc can reload the environment immediately when that specific file is modified. A is wrong because SessionEnd fires when the session is terminating, which is too late to refresh the environment for the current session's remaining work. B is wrong because CwdChanged alone misses the initial load at session start, meaning the environment may not be set correctly for the first directory Claude works in. D is wrong because PostCompact fires after conversation history is compacted, which is unrelated to environment file changes. (source: Hooks guide)

</details>

---

## Question 7
What does `UserPromptExpansion` fire on?

A) Any stop token
B) Tool failure only
C) User command expansion into a prompt before Claude sees it
D) MCP tool completion

<details>
<summary>Answer</summary>

**C)** UserPromptExpansion fires when a user's slash command or shorthand is being expanded into the full prompt text, giving the hook an opportunity to inspect or modify the expanded content before it is passed to Claude. A is wrong because stop tokens trigger the Stop or StopFailure events, not UserPromptExpansion. B is wrong because tool failures trigger PostToolUse or related events, not UserPromptExpansion. D is wrong because MCP tool completion would fire PostToolUse events, not UserPromptExpansion. (source: Hooks guide)

</details>

---

## Question 8
You need a long-running background test after every edit without blocking the turn. Use:

A) `type: prompt` + `async: true`
B) `type: command` + `async: true`
C) `type: mcp_tool` + `async: true`
D) `type: http` + `decision: defer`

<details>
<summary>Answer</summary>

**B)** The async: true flag is a feature of command-type hooks; setting it causes Claude Code to launch the command process and immediately continue the turn without waiting for the process to exit, making it ideal for long-running test suites that should not block the model. A is wrong because async: true is not a supported field for prompt-type hooks, which inject text into the conversation context and have different execution semantics. C is wrong because async: true is not a supported field for mcp_tool-type hooks; MCP tool hooks invoke a server-side tool and wait for a response. D is wrong because http-type hooks do not have a "decision: defer" field; the async pattern for non-blocking execution is specific to command hooks. (source: Hooks guide)

</details>

---

## Question 9
Can async hooks block a tool call with `permissionDecision: deny`?

A) Yes, always
B) Only on weekends
C) No, async cannot control already-proceeded action
D) Only for Bash

<details>
<summary>Answer</summary>

**C)** When a hook runs asynchronously, Claude Code does not wait for its output before proceeding with the tool call. By the time an async hook finishes and returns a permissionDecision, the action has already been taken, so deny has no effect. A is wrong because an async hook's output is not read before the tool executes, so a deny decision arrives too late to block anything. B is wrong because hook behavior does not vary by day of the week; this is not a real constraint. D is wrong because the limitation applies to all tool types, not just Bash; async hooks cannot block any tool call regardless of the tool involved. (source: Hooks guide)

</details>

---

## Question 10
You need to trigger a webhook for compliance checks and include auth token from env. Best type?

A) `prompt`
B) `agent`
C) `http` with `headers` and `allowedEnvVars`
D) `mcp_tool` only

<details>
<summary>Answer</summary>

**C)** The http hook type sends an HTTP POST to a specified URL and supports a headers field for setting authorization headers, as well as allowedEnvVars to safely interpolate environment variables (such as an auth token) into those headers without hardcoding secrets in the config file. A is wrong because prompt hooks inject text into the Claude conversation context and cannot make outbound HTTP calls to external webhooks. B is wrong because agent hooks invoke a sub-agent and are designed for judgment-heavy tasks, not for straightforward webhook delivery with auth headers. D is wrong because mcp_tool hooks call a tool on a connected MCP server, not an arbitrary external webhook endpoint. (source: Hooks guide)

</details>

---

## Question 11
What happens if an HTTP hook returns non-2xx?

A) Session hard-stops
B) Tool call always denied
C) Non-blocking error; execution continues
D) Claude retries forever

<details>
<summary>Answer</summary>

**C)** A non-2xx HTTP response from a hook is treated as a non-blocking error; Claude Code logs the failure and continues execution as if the hook had not fired, unless a valid 2xx response was returned with a blocking permissionDecision payload. A is wrong because a hook HTTP error does not terminate the session; only a permissionDecision of deny in a 2xx response can block execution. B is wrong because a non-2xx response carries no decision payload at all — the tool call is not denied, it proceeds normally. D is wrong because Claude Code does not retry failed HTTP hooks; it logs the error and moves on without retry logic. (source: Hooks guide)

</details>

---

## Question 12
You want to call an existing MCP server tool after `Write`. Best type?

A) `command`
B) `http`
C) `mcp_tool`
D) `prompt`

<details>
<summary>Answer</summary>

**C)** The mcp_tool hook type is specifically designed to invoke a tool on a connected MCP server, allowing hooks to leverage the same server tools already available to Claude without spawning shell processes or making separate HTTP calls. A is wrong because a command hook runs a local shell command or binary, not an MCP server tool; you would need to reimplement MCP client logic in a shell script. B is wrong because an http hook makes a plain HTTP request to a URL, not an MCP protocol call to a connected server tool. D is wrong because a prompt hook injects text into the conversation context and cannot directly invoke an MCP server tool. (source: Hooks guide)

</details>

---

## Question 13
An MCP tool hook is configured on `SessionStart` and fails with "server not connected." Why?

A) MCP tools are disabled for hooks
B) `SessionStart` can fire before MCP connections finish
C) Wrong event name only
D) Must use `prompt` first

<details>
<summary>Answer</summary>

**B)** SessionStart fires very early in the session lifecycle, and MCP server connections are established asynchronously after session initialization begins. If the hook fires before the MCP server has finished connecting, any mcp_tool invocation will fail because the server is not yet available. A is wrong because MCP tools are supported for hooks; the issue is timing, not a blanket prohibition. C is wrong because the event name SessionStart is valid and correct; the failure is due to connection timing, not a typo. D is wrong because using a prompt hook first would not solve the MCP connection timing issue; it would just inject text before the server is ready. (source: Hooks guide)

</details>

---

## Question 14
For `FileChanged` watch list, matcher behavior is:

A) Always regex
B) Literal filename list split by `|`
C) Ignored
D) Derived from `if`

<details>
<summary>Answer</summary>

**B)** For FileChanged events, the matcher field is interpreted as a literal list of filenames or paths separated by the pipe character, not as a regex pattern, so the hook fires only when one of the explicitly listed files changes. A is wrong because unlike the tool-name matcher for events like PreToolUse and PostToolUse, the FileChanged matcher does not use regex — it uses literal filename matching. C is wrong because the matcher is not ignored for FileChanged; it is the primary mechanism for specifying which files to watch. D is wrong because the if field is a separate conditional expression evaluated after the matcher; the matcher is not derived from the if field. (source: Hooks guide)

</details>

---

## Question 15
Which event has no matcher support and fires every occurrence?

A) `PostToolUse`
B) `PermissionRequest`
C) `TaskCreated`
D) `ConfigChange`

<details>
<summary>Answer</summary>

**C)** TaskCreated does not support a matcher field and fires on every task creation event without filtering, making it unsuitable for selective triggering — any hook on TaskCreated will run for every new task. A is wrong because PostToolUse supports a matcher field that can filter by tool name using a regex pattern, allowing selective firing. B is wrong because PermissionRequest supports filtering by the type of permission being requested, so hooks can be scoped to specific permission types. D is wrong because ConfigChange fires when settings are modified and does support filtering by which setting changed, so it is not an always-fire event. (source: Hooks guide)

</details>

---

## Question 16
Best event to capture all parallel tool calls completion before next model step:

A) `PostToolBatch`
B) `PostToolUseFailure`
C) `Stop`
D) `Setup`

<details>
<summary>Answer</summary>

**A)** PostToolBatch fires once after all tools in a parallel tool call batch have completed, providing a single checkpoint where the hook can inspect all results together before the model processes them, rather than firing once per individual tool completion. B is wrong because PostToolUseFailure (or the failure variant of PostToolUse) fires per individual failed tool, not after the entire batch has finished, so it does not provide a batch-level checkpoint. C is wrong because Stop fires at the end of the entire turn, not between parallel tool batches and the next model reasoning step within the same turn. D is wrong because Setup is not a standard hook event in the Claude Code hooks system; there is no event by that name. (source: Hooks guide)

</details>

---

## Question 17
In `PreToolUse`, multiple hooks return conflicting decisions. Which precedence is most restrictive?

A) `allow` wins
B) `ask` wins over deny
C) `deny` wins
D) Last hook wins

<details>
<summary>Answer</summary>

**C)** When multiple PreToolUse hooks return conflicting permissionDecision values, the most restrictive decision wins: deny takes precedence over ask, and ask takes precedence over allow, ensuring that no single hook can silently override a security restriction set by another hook. A is wrong because allow is the least restrictive decision and loses to both ask and deny when there is a conflict. B is wrong because ask prompts the user for a decision but is less restrictive than an outright deny; deny still wins over ask. D is wrong because last-hook-wins would allow any single hook to override security restrictions set by earlier hooks, which would undermine the safety model. (source: Hooks guide)

</details>

---

## Question 18
You want to enrich context after compaction with project conventions. Useful pattern:

A) `SessionStart` matcher `compact` that prints context to stdout
B) `StopFailure` deny
C) `PermissionDenied` retry
D) `TaskCompleted` only

<details>
<summary>Answer</summary>

**A)** The PostCompact event (or a SessionStart hook scoped to post-compaction) fires after conversation history is compacted, and a hook can print project conventions or context to stdout so Claude Code injects that text back into the conversation, restoring critical context that was compressed away. B is wrong because StopFailure fires when a turn ends due to an API or execution error, not after compaction, and returning deny from StopFailure cannot inject context into a new conversation window. C is wrong because PermissionDenied fires when a specific permission is denied and its retry signal is for retrying that tool call, not for injecting project context after compaction. D is wrong because TaskCompleted fires when an agent task finishes, not after conversation compaction, so it would not trigger at the right lifecycle point. (source: Hooks guide)

</details>

---

## Question 19
What is `TeammateIdle` mainly useful for?

A) Blocking shell commands
B) Tracking/automating around agent-team inactivity transitions
C) Forcing compaction
D) Changing model temperature

<details>
<summary>Answer</summary>

**B)** TeammateIdle fires when an agent in a multi-agent team transitions to an idle state, making it useful for orchestration patterns like reassigning work, sending notifications, or triggering cleanup tasks when a teammate stops being active. A is wrong because blocking shell commands is the domain of PreToolUse hooks with a Bash matcher and permissionDecision deny, not TeammateIdle. C is wrong because compaction is triggered by conversation length thresholds and the PostCompact event handles post-compaction logic; TeammateIdle has no mechanism to force compaction. D is wrong because model temperature and other inference parameters are set at request time in the API call, not through hook events during a session. (source: Hooks guide)

</details>

---

## Question 20
`PermissionDenied` event can signal model to try again with:

A) `{continue: true}`
B) `{retry: true}`
C) `{decision: "allow"}`
D) `{tool_retry: 1}`

<details>
<summary>Answer</summary>

**B)** A PermissionDenied hook can return a JSON payload containing retry: true, which signals Claude Code to present the model with the denial context and allow it to attempt the operation again with a modified approach. A is wrong because continue: true is not a recognized field in the PermissionDenied hook response schema; the correct field name is retry. C is wrong because returning decision: "allow" in a PermissionDenied hook does not retroactively change the permission outcome; the denial has already occurred and the allow decision field is used in PermissionRequest hooks, not PermissionDenied. D is wrong because tool_retry: 1 is not a valid field in the hooks response schema; there is no such counter-based retry mechanism. (source: Hooks guide)

</details>

---

## Question 21
You need policy decisions that require judgment (not deterministic shell checks). Prefer:

A) `prompt` or `agent` hooks
B) `CwdChanged` only
C) `WorktreeRemove`
D) `Notification` with bell

<details>
<summary>Answer</summary>

**A)** Prompt hooks inject instructions into Claude's context so the model can apply nuanced reasoning to a policy decision, and agent hooks spawn a sub-agent that can reason about complex conditions — both are appropriate when deterministic shell logic is insufficient for the judgment required. B is wrong because CwdChanged is a lifecycle event that fires when the working directory changes; it is not a hook type suited for policy judgment and does not have a mechanism to make approval decisions. C is wrong because WorktreeRemove fires when a git worktree is being removed; it is a lifecycle event for that specific operation, not a general-purpose hook type for policy evaluation. D is wrong because Notification hooks fire when Claude sends a notification and cannot themselves perform policy judgment or block tool execution based on complex reasoning. (source: Hooks guide)

</details>

---

## Question 22
Best reason to keep hook matchers narrow:

A) Prevent JSON parse cost only
B) Avoid accidental broad approvals/actions and reduce blast radius
C) Required by MCP protocol
D) To enable async mode

<details>
<summary>Answer</summary>

**B)** Narrow matchers ensure a hook fires only for the specific tool events it was designed for, preventing it from accidentally approving, denying, or running side effects on unrelated tool calls and reducing the scope of potential misconfigurations or security oversights. A is wrong because JSON parsing cost is negligible compared to the safety and correctness benefits; the primary reason for narrow matchers is not performance but blast radius control. C is wrong because the MCP protocol has no requirement about hook matcher specificity; matcher scope is a Claude Code configuration concern, not a protocol mandate. D is wrong because async mode is enabled by the async: true field on a command hook and has no dependency on whether the matcher is narrow or broad. (source: Hooks guide)

</details>

---

## Question 23
`StopFailure` semantics:

A) Can be blocked with exit code 2
B) Output and exit code are ignored; turn ended by API error
C) Same as `Stop`
D) Runs only in plan mode

<details>
<summary>Answer</summary>

**B)** StopFailure fires after a turn has already ended due to an API or execution error, so Claude Code does not read the hook's output or exit code to make any decisions — the turn is already over and the failure has already occurred, making the hook useful only for side effects like logging or alerting. A is wrong because exit code 2 (the deny signal) is meaningful in PreToolUse hooks to block tool execution, but StopFailure has no pending action to block; the turn has already ended. C is wrong because Stop fires after a successful turn completion and its output can influence context injection for the next turn, whereas StopFailure fires after an error and its output is ignored. D is wrong because StopFailure is not scoped to plan mode; it fires whenever any turn ends due to failure, regardless of the current mode. (source: Hooks guide)

</details>

---

## Question 24
To distribute vetted hooks org-wide while blocking user/project hooks, admins rely on:

A) `allowManagedHooksOnly` and managed settings
B) `disableAllHooks` in local settings
C) Session aliases
D) FileChanged watch

<details>
<summary>Answer</summary>

**A)** The allowManagedHooksOnly flag in managed (enterprise) settings restricts hook execution to only those hooks defined in the managed settings layer, preventing users from adding project-level or user-level hooks that could bypass org policy while still allowing centrally vetted hooks to run. B is wrong because disableAllHooks would block the org-vetted hooks as well as user hooks, defeating the purpose of distributing managed hooks — it is a total kill switch, not a selective trust mechanism. C is wrong because session aliases are a CLI convenience feature for reusing session configurations and have no role in hook trust scope enforcement. D is wrong because FileChanged watch is a hook event for responding to file system changes, not a mechanism for controlling hook authorization scope across an organization. (source: Claude Code settings)

</details>

---

## Question 25
Where should a shareable project hook live?

A) `~/.claude/settings.json`
B) `.claude/settings.local.json`
C) `.claude/settings.json`
D) temporary `/tmp/hook.json`

<details>
<summary>Answer</summary>

**C)** `.claude/settings.json` is the project-level settings file that is committed to version control alongside the codebase, making any hooks defined there automatically available to all team members who clone the repository. A is wrong because `~/.claude/settings.json` is the user-level global settings file on the individual developer's machine and is not shared with other team members. B is wrong because `.claude/settings.local.json` is explicitly intended for local overrides that should not be committed to version control (it is typically gitignored), making it the wrong place for shared project hooks. D is wrong because a temporary file in /tmp is not part of the project, is not version-controlled, and will not persist across sessions or machines. (source: Claude Code settings)

</details>

---

## Question 26
When should you use `WorktreeCreate` hook?

A) Only to run prettier
B) To replace/customize default git worktree behavior (especially non-git VCS)
C) To disable MCP
D) To force teammate mode

<details>
<summary>Answer</summary>

**B)** WorktreeCreate fires when Claude Code is about to create a new worktree, and a hook can override or customize that behavior — which is especially valuable for non-git version control systems or repositories with non-standard worktree setups that Claude Code's default git worktree command would handle incorrectly. A is wrong because running a formatter like prettier is a PostToolUse concern triggered by file edit events, not a worktree lifecycle concern; using WorktreeCreate for formatting would be both incorrect and fragile. C is wrong because MCP server connections are managed through the MCP configuration section of settings, not through worktree lifecycle hooks. D is wrong because teammate mode is an agent orchestration configuration, not something triggered or enabled through the WorktreeCreate hook event. (source: Hooks guide)

</details>

---

## Question 27
What does `Notification` hook event represent?

A) All Bash command output
B) Claude sending a notification (permission prompt, idle prompt, etc.)
C) MCP server startup
D) CWD mutation

<details>
<summary>Answer</summary>

**B)** The Notification event fires whenever Claude Code sends a notification to the user, including permission prompts, idle state alerts, and other informational messages, allowing hooks to intercept, log, or react to these notification moments. A is wrong because Bash command output is not surfaced as a Notification event; Bash tool execution produces PostToolUse events, and the command's stdout/stderr is part of the tool result, not a notification. C is wrong because MCP server startup is a session initialization concern and does not fire a Notification event; SessionStart is the closest lifecycle event for early-session activities. D is wrong because CWD changes fire the CwdChanged event, not the Notification event; these are distinct lifecycle signals for different system state changes. (source: Hooks guide)

</details>

---

## Question 28
Why is "prompt instructions only" weaker than programmatic hooks for critical constraints?

A) Prompt is invalid JSON
B) Prompt-based behavior is probabilistic; hooks are deterministic execution points
C) Hooks are cheaper tokens
D) Prompts cannot mention tools

<details>
<summary>Answer</summary>

**B)** A language model follows prompt instructions with high but not perfect probability — under unusual inputs, edge cases, or adversarial prompts, it may fail to comply even with explicit instructions. Hooks, by contrast, are deterministic execution points in the Claude Code runtime: a PreToolUse hook that returns deny will always block the tool call, regardless of what the model was prompted to do. A is wrong because prompts are plain text, not JSON, so JSON validity is irrelevant; the limitation is probabilistic compliance, not a syntax issue. C is wrong because while hooks do not consume prompt tokens, the reason to prefer hooks for critical constraints is reliability and determinism, not token economics. D is wrong because prompts can and do mention tools by name; the limitation is not what prompts can reference but whether the model reliably acts on those references. (source: Hooks guide)

</details>

---

## Question 29
You want to watch settings edits for audit trail during active sessions. Use:

A) `ConfigChange`
B) `UserPromptSubmit`
C) `SessionEnd`
D) `PreCompact`

<details>
<summary>Answer</summary>

**A)** ConfigChange fires whenever Claude Code detects a change to its settings files during an active session, making it the correct event to hook into for building an audit trail of configuration modifications as they happen. B is wrong because UserPromptSubmit fires when the user submits a message, which has nothing to do with settings file modifications; it cannot detect when settings are changed. C is wrong because SessionEnd fires when the session terminates, which would only capture that a session ended, not which settings were changed or when during the session they were modified. D is wrong because PreCompact is not a standard Claude Code hook event; the compaction-related event is PostCompact, and neither is related to settings file auditing. (source: Hooks guide)

</details>

---

## Question 30
`stdin`/`stdout` vs HTTP body in hooks:

A) Command hooks: stdin/stdout; HTTP hooks: POST body/response body
B) Command hooks use only stderr
C) HTTP hooks read stdin directly
D) Both ignore JSON

<details>
<summary>Answer</summary>

**A)** Command hooks receive their event context JSON on stdin and write their response JSON to stdout, while HTTP hooks receive their event context as the HTTP POST request body and return their response in the HTTP response body — each transport model is consistent with its underlying mechanism. B is wrong because command hooks use stdin for input and stdout for output; stderr is available for error logging but is not the primary transport channel for hook data. C is wrong because HTTP hooks operate over the network using HTTP request/response semantics; they do not read from the process's stdin stream because they are not shell processes. D is wrong because both command hooks and HTTP hooks communicate exclusively through JSON — the hook event payload is JSON, and the expected response format is also JSON. (source: Hooks guide)

</details>

---
