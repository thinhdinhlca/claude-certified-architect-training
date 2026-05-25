# CCA Hooks Quiz - Domain 1 Hooks & Workflow Control

Format: scenario-based multiple choice (A-D), one best answer per question.  
Target: pass threshold mindset (`>= 720`) with immediate retest on misses.

## Questions

### Q1
You need to ensure formatting always runs after file edits, regardless of model behavior. Best hook pattern?
A. `UserPromptSubmit` with prompt reminder  
B. `PostToolUse` matcher `Edit|Write` + formatter command  
C. `Stop` hook with manual checklist  
D. `Notification` hook

### Q2
A teammate asks what stream command hooks read input from. Correct answer?
A. `stdout`  
B. `stderr`  
C. `stdin`  
D. HTTP response body

### Q3
You want to deny destructive Bash commands before execution. Best event?
A. `PostToolUse`  
B. `PreToolUse`  
C. `Stop`  
D. `SessionEnd`

### Q4
Why use `matcher: "Bash"` and `if: "Bash(rm *)"` together?
A. Required by JSON parser  
B. `matcher` is regex only, `if` is exact only  
C. Coarse filter first, precise argument-level filter second  
D. `if` replaces `matcher`

### Q5
You need to auto-approve only `ExitPlanMode` permission prompts. Which event?
A. `PermissionRequest`  
B. `PermissionDenied`  
C. `UserPromptExpansion`  
D. `StopFailure`

### Q6
You changed `.envrc` and want Claude environment refreshed automatically. Best hook setup?
A. `SessionEnd` only  
B. `CwdChanged` only  
C. `SessionStart` + `CwdChanged` (+ optional `FileChanged` watch)  
D. `PostCompact`

### Q7
What does `UserPromptExpansion` fire on?
A. Any stop token  
B. Tool failure only  
C. User command expansion into a prompt before Claude sees it  
D. MCP tool completion

### Q8
You need a long-running background test after every edit without blocking the turn. Use:
A. `type: prompt` + `async: true`  
B. `type: command` + `async: true`  
C. `type: mcp_tool` + `async: true`  
D. `type: http` + `decision: defer`

### Q9
Can async hooks block a tool call with `permissionDecision: deny`?
A. Yes, always  
B. Only on weekends  
C. No, async cannot control already-proceeded action  
D. Only for Bash

### Q10
You need to trigger a webhook for compliance checks and include auth token from env. Best type?
A. `prompt`  
B. `agent`  
C. `http` with `headers` and `allowedEnvVars`  
D. `mcp_tool` only

### Q11
What happens if an HTTP hook returns non-2xx?
A. Session hard-stops  
B. Tool call always denied  
C. Non-blocking error; execution continues  
D. Claude retries forever

### Q12
You want to call an existing MCP server tool after `Write`. Best type?
A. `command`  
B. `http`  
C. `mcp_tool`  
D. `prompt`

### Q13
An MCP tool hook is configured on `SessionStart` and fails with “server not connected.” Why?
A. MCP tools are disabled for hooks  
B. `SessionStart` can fire before MCP connections finish  
C. Wrong event name only  
D. Must use `prompt` first

### Q14
For `FileChanged` watch list, matcher behavior is:
A. Always regex  
B. Literal filename list split by `|`  
C. Ignored  
D. Derived from `if`

### Q15
Which event has no matcher support and fires every occurrence?
A. `PostToolUse`  
B. `PermissionRequest`  
C. `TaskCreated`  
D. `ConfigChange`

### Q16
Best event to capture all parallel tool calls completion before next model step:
A. `PostToolBatch`  
B. `PostToolUseFailure`  
C. `Stop`  
D. `Setup`

### Q17
In `PreToolUse`, multiple hooks return conflicting decisions. Which precedence is most restrictive?
A. `allow` wins  
B. `ask` wins over deny  
C. `deny` wins  
D. Last hook wins

### Q18
You want to enrich context after compaction with project conventions. Useful pattern:
A. `SessionStart` matcher `compact` that prints context to stdout  
B. `StopFailure` deny  
C. `PermissionDenied` retry  
D. `TaskCompleted` only

### Q19
What is `TeammateIdle` mainly useful for?
A. Blocking shell commands  
B. Tracking/automating around agent-team inactivity transitions  
C. Forcing compaction  
D. Changing model temperature

### Q20
`PermissionDenied` event can signal model to try again with:
A. `{continue: true}`  
B. `{retry: true}`  
C. `{decision: "allow"}`  
D. `{tool_retry: 1}`

### Q21
You need policy decisions that require judgment (not deterministic shell checks). Prefer:
A. `prompt` or `agent` hooks  
B. `CwdChanged` only  
C. `WorktreeRemove`  
D. `Notification` with bell

### Q22
Best reason to keep hook matchers narrow:
A. Prevent JSON parse cost only  
B. Avoid accidental broad approvals/actions and reduce blast radius  
C. Required by MCP protocol  
D. To enable async mode

### Q23
`StopFailure` semantics:
A. Can be blocked with exit code 2  
B. Output and exit code are ignored; turn ended by API error  
C. Same as `Stop`  
D. Runs only in plan mode

### Q24
To distribute vetted hooks org-wide while blocking user/project hooks, admins rely on:
A. `allowManagedHooksOnly` and managed settings  
B. `disableAllHooks` in local settings  
C. Session aliases  
D. FileChanged watch

### Q25
Where should a shareable project hook live?
A. `~/.claude/settings.json`  
B. `.claude/settings.local.json`  
C. `.claude/settings.json`  
D. temporary `/tmp/hook.json`

### Q26
When should you use `WorktreeCreate` hook?
A. Only to run prettier  
B. To replace/customize default git worktree behavior (especially non-git VCS)  
C. To disable MCP  
D. To force teammate mode

### Q27
What does `Notification` hook event represent?
A. All Bash command output  
B. Claude sending a notification (permission prompt, idle prompt, etc.)  
C. MCP server startup  
D. CWD mutation

### Q28
Why is “prompt instructions only” weaker than programmatic hooks for critical constraints?
A. Prompt is invalid JSON  
B. Prompt-based behavior is probabilistic; hooks are deterministic execution points  
C. Hooks are cheaper tokens  
D. Prompts cannot mention tools

### Q29
You want to watch settings edits for audit trail during active sessions. Use:
A. `ConfigChange`  
B. `UserPromptSubmit`  
C. `SessionEnd`  
D. `PreCompact`

### Q30
`stdin`/`stdout` vs HTTP body in hooks:
A. Command hooks: stdin/stdout; HTTP hooks: POST body/response body  
B. Command hooks use only stderr  
C. HTTP hooks read stdin directly  
D. Both ignore JSON

---

## Answer Key + Why

1. **B** - Deterministic post-edit formatter path.  
2. **C** - Command hook input arrives on stdin.  
3. **B** - `PreToolUse` is pre-execution control point.  
4. **C** - Two-stage filtering improves precision and cost.  
5. **A** - Permission dialog interception event.  
6. **C** - Start + directory-change reloading pattern.  
7. **C** - Expansion occurs before Claude consumes the final prompt.  
8. **B** - Async is command-hook feature.  
9. **C** - Async cannot block/deny completed action path.  
10. **C** - HTTP hooks + env interpolation controls.  
11. **C** - HTTP hook failures are non-blocking unless 2xx decision payload blocks.  
12. **C** - MCP server tool invocation hook type.  
13. **B** - Connection timing issue at early lifecycle events.  
14. **B** - FileChanged uses literal watch-list behavior.  
15. **C** - `TaskCreated` has no matcher support.  
16. **A** - Batch-level post-parallel checkpoint.  
17. **C** - Most restrictive precedence applies.  
18. **A** - Known compaction context reinjection pattern.  
19. **B** - Team runtime orchestration signal.  
20. **B** - `retry: true` for denied tool-call retry eligibility.  
21. **A** - Judgment-heavy checks fit prompt/agent hooks.  
22. **B** - Narrow scope avoids overreach and unsafe automation.  
23. **B** - StopFailure output/exit ignored due already-failed turn.  
24. **A** - Managed policy controls trusted hook scope.  
25. **C** - Project-shareable config location.  
26. **B** - Worktree lifecycle customization, including non-git flows.  
27. **B** - Notification lifecycle event.  
28. **B** - Deterministic hook execution beats probabilistic prompt compliance for critical rules.  
29. **A** - Dedicated config-change event.  
30. **A** - Correct transport mapping.

---

## Retest Protocol

1. Run this quiz manually and mark misses.
2. Re-read source sections for each miss.
3. Immediately retest until you can explain each wrong option.

Sources:
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/settings#hook-configuration
