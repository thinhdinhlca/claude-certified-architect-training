# Error Propagation — Question Bank

## Question 1
A web search subagent returns two types of non-success outcomes: an HTTP 504 timeout on one query and a valid API response containing `{"results": [], "total": 0}` on another. The coordinator receives both and must decide next steps. Which approach correctly handles these distinct outcomes?

A) Aggregate both into a single "search failure" metric and retry the affected queries uniformly
B) Treat the 504 as a retryable access failure and treat the empty results as a valid informative finding requiring no retry
C) Return a generic "search unavailable" error for both to simplify coordinator logic
D) Retry both immediately since neither produced usable content for the final report

<details>
<summary>Answer</summary>

**B)** A 504 timeout is an access failure — the data may exist but was unreachable, making a retry appropriate. Zero results is a valid semantic outcome — the search succeeded and found nothing, which is itself informative. Conflating them destroys the semantic distinction. A is wrong because merging both into a single metric causes unnecessary retries on valid empty results and potentially masks persistent access failures. C is wrong because returning a generic error loses both the access failure context (needed for intelligent retry) and the valid empty-result finding (informative data about the research domain). D is wrong because retrying a successful "0 results" query wastes resources and misrepresents the outcome as an error when it is a legitimate finding. (source: Agentic loop)

</details>

---

## Question 2
A document analysis subagent encounters a corrupted PDF that cannot be parsed. The subagent has already attempted two parsing strategies without success. Which error handling approach is most appropriate?

A) Silently skip the document and continue processing the remaining files
B) Terminate the entire workflow to prevent any partial results from entering the output
C) Retry the same parsing strategies with exponential backoff until the document succeeds
D) Return a structured error to the coordinator with the document identifier, failure type, and the two attempted strategies

<details>
<summary>Answer</summary>

**D)** A corrupted file is not a transient error — retrying the same strategies will not succeed. The coordinator has broader context to decide whether to skip, attempt alternative parsing, or notify the user; structured error context enables that decision. A is wrong because silent skip hides the failure, leaving the coordinator unaware of the gap and unable to make an informed recovery decision. B is wrong because terminating the workflow kills all progress already made on other documents — a single corrupted file does not justify discarding the entire job. C is wrong because corruption is a persistent failure, not a transient one; exponential backoff on a fundamentally broken file wastes time and produces no new information. (source: Agentic loop)

</details>

---

## Question 3
Your system classifies errors into three categories: tool execution errors (the tool ran but returned an error), model behavior errors (the model generated incorrect tool arguments), and orchestration errors (the coordinator failed to route tasks correctly). A subagent calls `search_academic_db` but receives `{"error": "rate_limit_exceeded", "retry_after": 30}`. Which category does this belong to, and what is the correct recovery owner?

A) Tool execution error — the subagent should handle this locally by waiting and retrying before escalating
B) Orchestration error — the coordinator should pause the entire pipeline until the rate limit resets
C) Model behavior error — the coordinator should update its prompt to prevent the subagent from calling rate-limited tools
D) Orchestration error — the coordinator should re-route this task to a different subagent with a lower-volume search tool

<details>
<summary>Answer</summary>

**A)** A rate limit error is a tool execution error: the tool ran, received a valid API response, and that response indicates a recoverable transient condition. The subagent is the lowest capable layer for handling it — waiting 30 seconds and retrying is a straightforward local recovery without coordinator involvement. B is wrong because pausing the entire pipeline is disproportionate; only the affected tool call needs to wait, and other parallel work can continue. C is wrong because this is not a model behavior error; the model correctly called a valid tool with valid arguments. The error is in the external API response, not in model reasoning. D is wrong because re-routing to a different subagent escalates unnecessarily — the original subagent can resolve this transiently without architectural changes. (source: Agentic loop)

</details>

---

## Question 4
A subagent's tool call fails with a JSON schema validation error: the tool expected `{"query": string, "max_results": integer}` but received `{"query": string, "max_results": "50"}`. The model passed the count as a string instead of an integer. Which error category is this, and what is the correct fix?

A) Tool execution error — retry the tool call immediately since schema errors are often transient
B) Model behavior error — update the tool description to emphasize that max_results must be an integer type
C) Orchestration error — the coordinator should validate all tool arguments before passing them to subagents
D) Tool execution error — add input sanitization in the tool handler to coerce string integers to integers

<details>
<summary>Answer</summary>

**B)** When the model passes the wrong type for a parameter, this is a model behavior error — the tool schema was not clear enough to guide correct argument construction. Updating the tool description (or using `strict: true` schema enforcement) addresses the root cause: ambiguous type signaling. A is wrong because schema validation errors are not transient — retrying the same call with the same arguments will produce the same error. C is wrong because pre-validation by the coordinator adds a layer of complexity without addressing why the model generated the wrong type in the first place. D is wrong because adding coercion in the tool handler treats the symptom, not the cause — the model will continue generating wrong types on other calls, and type coercion can mask legitimate errors. (source: Tool use)

</details>

---

## Question 5
A multi-agent research system has three error types observed in production: (1) a subagent's web search tool returns HTTP 429 (rate limited), (2) a subagent returns results from a source the coordinator did not request, and (3) the coordinator routes a task to the wrong subagent because two tools have similar names. Match each error to its correct category: tool execution, model behavior, orchestration.

A) 1=model behavior, 2=orchestration, 3=tool execution
B) 1=orchestration, 2=model behavior, 3=tool execution
C) 1=tool execution, 2=orchestration, 3=model behavior
D) 1=tool execution, 2=model behavior, 3=orchestration

<details>
<summary>Answer</summary>

**D)** HTTP 429 is a tool execution error — the tool ran and the external API rejected it; retry logic in the subagent is the correct response. Returning results from an unrequested source is a model behavior error — the model made an autonomous decision to query a different source, which is a reasoning or instruction-following issue. Misrouting due to similar tool names is an orchestration error — the coordinator was confused by ambiguous tool descriptions, causing a routing failure. A is wrong because a 429 rate limit is caused by tool execution, not by the coordinator's routing logic. B is wrong because returning wrong-source results is a model behavior issue, not an orchestration routing decision. C is wrong because tool name ambiguity causing misrouting is an orchestration-layer problem, not a raw tool execution failure or model behavior error. (source: Agentic loop)

</details>

---

## Question 6
A coordinator receives the following error payload from a subagent: `{"status": "error", "message": "Search failed"}`. The coordinator cannot determine whether to retry, reroute, or skip. What is the minimum additional structure the subagent should include to enable intelligent recovery?

A) Include error type (access_failure vs not_found), the attempted query, whether the error is recoverable, and any partial results obtained
B) Add an HTTP status code so the coordinator can apply standard HTTP retry semantics
C) Add a timestamp and request ID so the coordinator can log the failure for audit purposes
D) Return the full stack trace from the tool execution so the coordinator can diagnose the root cause

<details>
<summary>Answer</summary>

**A)** Intelligent recovery requires: error type (determines retry vs skip strategy), the attempted query (enables modified retry), recoverability flag (prevents futile retries on persistent failures), and partial results (preserves value from what succeeded). These four fields give the coordinator everything it needs to make an informed decision. B is wrong because HTTP status codes apply only to HTTP tool calls and collapse the semantic distinction between different failure modes. C is wrong because timestamps and request IDs serve logging and auditing purposes but provide no information the coordinator needs to choose a recovery strategy. D is wrong because stack traces expose implementation internals that the coordinator cannot act on — the coordinator needs semantic error information, not debugging artifacts. (source: Agentic loop)

</details>

---

## Question 7
A subagent encounters a transient database connection error on its first attempt. The subagent has a retry policy configured. At what point should the subagent escalate to the coordinator rather than continuing local retries?

A) Immediately for any error that occurs more than once within a single task execution
B) After exhausting local retries or determining the error is persistent, returning the final error state with context about what was attempted
C) After the first failure, to give the coordinator maximum time to find an alternative
D) Never — the subagent should retry indefinitely until it succeeds or the overall task times out

<details>
<summary>Answer</summary>

**B)** The principle of handling errors at the lowest capable layer means the subagent should resolve transient failures locally. Escalation is correct when retries are exhausted or the error is identified as persistent — at that point, the subagent returns structured context (what was attempted, how many times, what the error was) so the coordinator can make an informed decision. A is wrong because two occurrences is not a reliable threshold for "persistent" — some transient errors may occur twice in rapid succession before resolving. C is wrong because escalating after the first failure is premature — it increases coordinator involvement unnecessarily for errors the subagent can resolve in seconds. D is wrong because indefinite retries without escalation can block the pipeline forever on persistent failures and prevent the coordinator from attempting alternative paths. (source: Agentic loop)

</details>

---

## Question 8
A web search subagent successfully queries three sources but fails on a fourth due to an access restriction. The subagent has partial results from the three successful sources. Which approach best applies local recovery principles?

A) Return the three successful results with a structured annotation indicating the fourth source was inaccessible and why
B) Return only a success flag since the subagent completed the majority of its work
C) Discard all results and return a failure, since incomplete results may mislead the coordinator
D) Retry the fourth source five more times before returning any results to the coordinator

<details>
<summary>Answer</summary>

**A)** Local recovery includes maximizing what can be recovered — three valid results are valuable partial output. The structured annotation on the fourth source tells the coordinator exactly what happened, enabling it to decide whether to attempt an alternative source or proceed with the available data. B is wrong because returning only a success flag without the failure annotation hides the gap — the coordinator cannot reason about coverage or decide whether to seek alternative sources. C is wrong because discarding successful results to maintain a "clean" all-or-nothing response abandons real value; partial results with transparency are more useful than nothing. D is wrong because an access restriction (not a transient error) will not resolve through retries — continuing to attempt it delays delivery of the three available results. (source: Agentic loop)

</details>

---

## Question 9
Three parallel research subagents are launched simultaneously. After 45 seconds, subagent A returns complete results, subagent B returns partial results with a coverage annotation, and subagent C returns `{"error": "timeout", "recoverable": true, "query": "climate policy EU 2024"}`. The coordinator must decide next steps. What is the correct approach?

A) Discard all results and relaunch all three subagents since the pipeline did not complete successfully
B) Wait for subagent C to self-recover before aggregating any results to ensure consistency
C) Proceed with A's complete results and B's annotated partial results; retry subagent C's query with the preserved query context
D) Use subagent A's results only and discard subagents B and C since their results are unreliable

<details>
<summary>Answer</summary>

**C)** Partial success should be handled by preserving all usable results. A's complete results and B's annotated partial results have clear value. C returned a recoverable error with the original query context — the coordinator can issue a targeted retry for that specific query without restarting the full pipeline. A is wrong because discarding all results to restart from scratch wastes the work of both A and B, which completed correctly — total reruns are only justified when results are corrupted or interdependent. B is wrong because "waiting for C to self-recover" is not a defined behavior — subagent C returned an error and will not automatically retry; the coordinator must issue the retry explicitly. D is wrong because B's partial results with coverage annotations are explicitly useful — the coordinator knows exactly what B covered and what it missed, enabling informed synthesis. (source: Agentic loop)

</details>

---

## Question 10
A coordinator orchestrates five subagents in parallel for a market research task. Subagents 1, 2, and 3 succeed. Subagent 4 returns a structured error with `"recoverable": false`. Subagent 5 returns a structured error with `"recoverable": true`. Which response best describes the correct coordinator behavior?

A) Halt the entire workflow since not all subagents completed successfully
B) Proceed using results from 1, 2, 3; mark subagent 4's domain as a permanent coverage gap; retry subagent 5's query
C) Retry both subagents 4 and 5 before proceeding to ensure maximum coverage
D) Discard subagent 4's domain from the final report without annotation to keep the output clean

<details>
<summary>Answer</summary>

**B)** The `recoverable` flag is the key discriminator: subagent 4's failure is permanent — retrying would waste resources and the gap should be annotated. Subagent 5's failure is recoverable — the coordinator should retry it with the preserved query context. Results from 1, 2, and 3 should be preserved regardless. A is wrong because halting on any non-complete subagent ignores the recoverable/unrecoverable distinction and discards substantial completed work. C is wrong because retrying a non-recoverable failure (subagent 4) is explicitly wasteful — the `recoverable: false` flag signals the error will persist. D is wrong because silently dropping subagent 4's domain without annotation hides a coverage gap from downstream synthesis, preventing informed confidence assessment. (source: Agentic loop)

</details>

---

## Question 11
A subagent should return errors via tool result content rather than by raising exceptions. A developer argues that raising an exception is equivalent since both stop execution. Why is the tool result approach preferred in multi-agent systems?

A) Tool result content is visible to the model in the conversation history; exceptions break the agentic loop and are not model-visible
B) Exceptions require the orchestrator to have access to the subagent's runtime, which is a security concern
C) Tool results can be retried automatically while exceptions require manual intervention
D) Exceptions are slower to process than structured tool results, so tool results reduce latency

<details>
<summary>Answer</summary>

**A)** The agentic loop depends on the model reasoning about tool outcomes. When a tool result contains error information, the model can read it, understand what happened, and decide the next action. An unhandled exception breaks the loop entirely — the model never sees what went wrong and cannot reason about recovery. B is wrong because exceptions do not require runtime access to the subagent — the concern is not security but model visibility into error state. C is wrong because neither mechanism provides automatic retry; retry logic must be explicitly implemented regardless of how the error is surfaced. D is wrong because the choice between exceptions and tool results is not about latency — both involve a round trip, and structured result serialization is not meaningfully slower than exception propagation. (source: Tool use)

</details>

---

## Question 12
A subagent's tool raises an unhandled Python exception: `requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected(...))`. The exception propagates and crashes the subagent process. From the coordinator's perspective, what information is lost compared to a structured error return?

A) Only the stack trace — the coordinator can infer the connection error and retry automatically
B) The error type classification, the recoverability flag, any partial results, and the query context that would have enabled targeted retry
C) Nothing — the coordinator receives the exception message as a string and can parse it for recovery context
D) Only the subagent's identity — the coordinator can reconstruct all other context from the task definition

<details>
<summary>Answer</summary>

**B)** An unhandled exception delivers a raw error string with no semantic structure. The coordinator loses: the explicit error type classification, the `recoverable` flag needed to decide whether to retry, any partial results the subagent had accumulated, and the preserved query context needed for a targeted retry. A is wrong because the stack trace does not encode recoverability or partial results; the coordinator cannot infer whether a retry is appropriate from exception text alone. C is wrong because parsing a raw exception message string for recovery semantics is fragile and error-prone — the coordinator cannot reliably extract structured intent from a free-form traceback. D is wrong because the query context preserved in a structured error often differs from the original task definition — the subagent may have reformulated the query before the failure. (source: Tool use)

</details>

---

## Question 13
A subagent tool handler catches an exception and returns the following in the tool result: `{"isError": true, "content": "An error occurred. Please try again."}`. The coordinator retries and fails again. What is the problem with this error return?

A) The subagent should not catch exceptions at all — they should propagate to the coordinator for centralized handling
B) The `isError` field is not a valid field in the tool result schema — errors should be returned as HTTP 500 responses
C) The message lacks error type, failure context, and recoverability signal — the coordinator cannot determine what went wrong or whether retry is appropriate
D) The error message is too long and should be shortened to reduce token usage in the coordinator's context

<details>
<summary>Answer</summary>

**C)** "Please try again" provides no actionable information: it does not specify what failed (network, auth, rate limit, schema), whether the error is transient or persistent, or what context would help a retry succeed. The coordinator retries blindly and fails again because it has no information to modify its approach. A is wrong because catching exceptions in the tool handler and returning structured errors is the correct pattern — unhandled exceptions break the agentic loop and are not model-visible. B is wrong because `isError` is a recognized field in tool result semantics used to signal errors to the model — the schema is not the problem here. D is wrong because the message is extremely short; the problem is insufficient information, not excessive length. (source: Tool use)

</details>

---

## Question 14
A financial research subagent is designed to return structured error objects. Which of the following error payloads best enables coordinator recovery for a failed database query?

A) `{"error": true, "code": 503}`
B) `{"status": "failed", "timestamp": "2026-05-24T10:30:00Z", "agent_id": "fin-001"}`
C) `{"error": "db_unavailable", "recoverable": true, "query": "SELECT revenue FROM q1_2026 WHERE company='ACME'", "partial_results": null, "retry_after_seconds": 15}`
D) `{"error": "DATABASE_ERROR", "stacktrace": "ConnectionPool.get() line 47: timeout after 30s..."}`

<details>
<summary>Answer</summary>

**C)** This payload contains every field the coordinator needs: error type (`db_unavailable`) for categorization, `recoverable: true` to confirm retry is worthwhile, the exact query to retry without re-derivation, null partial results to signal nothing was recovered, and a concrete `retry_after_seconds` to schedule the retry appropriately. A is wrong because an HTTP code alone provides no semantic context about what query failed, whether it is recoverable, or when to retry — 503 could mean anything from network partition to planned maintenance. B is wrong because timestamp and agent ID are audit fields, not recovery fields — they tell you when and who, not what failed and whether it can succeed on retry. D is wrong because a stack trace exposes implementation internals that the coordinator cannot act on and clutters the model's context with non-actionable debugging information. (source: Tool use)

</details>

---

## Question 15
A synthesis subagent receives research from five upstream subagents. Two subagents returned complete results, two returned partial results with coverage annotations, and one returned an unrecoverable error. The synthesis subagent's output should:

A) Return an error to the coordinator since the input is incomplete and synthesis cannot be trusted
B) Synthesize all available results with coverage annotations indicating which topic areas are well-supported, which are partially covered, and which have no coverage
C) Ask the coordinator to retry the failed subagent before proceeding with any synthesis
D) Only synthesize the two complete results and ignore the partial and failed results to ensure output quality

<details>
<summary>Answer</summary>

**B)** Graceful degradation with transparency: synthesize what is available and annotate coverage gaps explicitly. This preserves the value of the four subagents that succeeded while giving downstream consumers precise confidence information about each topic area. A is wrong because returning an error abandons all completed work for a single unrecoverable failure — partial synthesis with transparent gaps is almost always more valuable than no synthesis. C is wrong because the failed subagent returned an unrecoverable error — requesting a retry on a non-recoverable failure wastes time and blocks output delivery without any realistic chance of success. D is wrong because discarding the partial results (which have explicit coverage annotations) wastes valid data — a partially covered topic is more informative than no coverage. (source: Agentic loop)

</details>

---

## Question 16
A coordinator receives research results from four parallel subagents. Subagent A covered "AI in healthcare." Subagent B covered "AI in finance." Subagent C covered "AI in education." Subagent D timed out. The synthesis step needs to cover all four domains. How should the coordinator annotate this partial success before passing to synthesis?

A) Retry D three times synchronously before proceeding, since synthesis cannot run without complete coverage
B) Remove D's domain from the synthesis scope and proceed as if it was never assigned
C) Pass all four domains to synthesis with a note that D failed, letting synthesis determine the impact
D) Pass results from A, B, and C with an explicit coverage annotation indicating D's assigned domain has zero coverage due to timeout, and include D's original query for potential retry

<details>
<summary>Answer</summary>

**D)** The coverage annotation must be explicit and structured: which domain has no coverage, why (timeout), and what was being searched (D's query). This gives the synthesis agent the exact information it needs to annotate its output and lets a human or downstream system decide whether to attempt recovery separately. A is wrong because D timed out, suggesting a persistent or load-based issue; three synchronous retries block the entire pipeline and may all fail the same way. B is wrong because removing D's domain without annotation silently narrows the research scope — any downstream reader would not know the topic was ever intended to be covered. C is wrong because "a note that D failed" is vague — the synthesis agent needs the specific domain gap, not just a generic failure notice, to produce properly annotated output. (source: Agentic loop)

</details>

---

## Question 17
A coordinator receives this from a subagent: `{"results": [...25 items...], "searched": ["arxiv", "pubmed"], "not_searched": ["ieee_xplore"], "reason_not_searched": "rate_limit_exceeded"}`. What does the `not_searched` annotation enable that a plain results array cannot?

A) It provides an audit trail for compliance purposes to verify which databases were queried
B) It prevents the subagent from being blamed if the final report has gaps in coverage
C) It enables the coordinator to reason about coverage gaps, attempt targeted recovery of missed sources, and accurately represent confidence in the synthesis
D) It allows the model to verify that the subagent used the correct search tools as specified

<details>
<summary>Answer</summary>

**C)** Coverage annotations transform a partial result into a transparent partial result. The coordinator now knows exactly what was searched (can assess quality) and what was not (can attempt targeted retry of `ieee_xplore` or annotate the gap). A plain results array only tells you what was found, not whether the search was complete. A is wrong because compliance audit trails are a side benefit, not the primary function — the annotation is for recovery reasoning, not logging. B is wrong because responsibility attribution is not a system concern; coverage annotations exist to enable recovery and transparent output, not to manage blame. D is wrong because verifying tool usage is an audit concern, not a recovery-enabling capability — the coordinator needs to know what gaps exist, not just which tools ran. (source: Agentic loop)

</details>

---

## Question 18
A research pipeline has three stages: collection subagents → synthesis subagent → validation subagent. The synthesis subagent completes successfully but the validation subagent detects that 40% of the citations are inaccessible. Which coverage annotation approach correctly handles this mid-pipeline partial failure?

A) Validation should retry all inaccessible citations synchronously before returning any results
B) Validation should silently drop the inaccessible citations and return a clean validated result
C) Validation should return an error causing the coordinator to rerun synthesis from scratch
D) Validation should return results with annotations distinguishing verified citations from unverified ones, including which citations could not be accessed and why

<details>
<summary>Answer</summary>

**D)** Coverage annotations at the validation layer mirror the same principle as at the collection layer: annotate what is known versus unknown with enough context to enable informed decisions. A 60% verified / 40% unverified split with explicit identification of the unverifiable citations is far more useful than a binary pass/fail. A is wrong because synchronously retrying all inaccessible citations blocks the pipeline; if the citations are unavailable due to paywalls, link rot, or server issues, retries will not resolve them. B is wrong because silently dropping 40% of citations produces a clean-looking but incomplete output — the coordinator and end user cannot assess the confidence level of the result. C is wrong because rerunning synthesis from scratch does not fix the validation problem — the same citations will be inaccessible after a second synthesis pass, and the work is wasted. (source: Agentic loop)

</details>

---

## Question 19
Five subagents run in parallel. Each subagent should search a different geographic region. After all complete, the coordinator notes that subagents 2 and 4 both searched "North America" despite being assigned distinct regions. Which coordination failure does this represent and how should it be prevented?

A) Tool execution error — add deduplication logic after all subagents return to merge duplicate results
B) Model behavior error in both subagents — add prompt examples showing the correct region assignment
C) Orchestration error in the coordinator's task decomposition — coordinator should explicitly assign non-overlapping region boundaries before delegation
D) Orchestration error — add a shared state ledger so subagents can check which regions have been claimed before starting

<details>
<summary>Answer</summary>

**C)** This is a coordinator decomposition failure: the coordinator did not specify clear, non-overlapping boundaries before delegation. Both subagents defaulted to "North America" because the instructions were ambiguous. The fix happens before work begins, not after. A is wrong because deduplication after the fact wastes the tokens and time spent on duplicate searches — it treats the symptom while the root cause (ambiguous task boundaries) remains. B is wrong because this is not a subagent reasoning failure — each subagent individually made a plausible interpretation of its instructions; the instructions themselves were the problem. D is wrong because a shared state ledger introduces complex coordination overhead and race conditions — pre-partitioning before delegation eliminates the need for runtime coordination entirely. (source: Agentic loop)

</details>

---

## Question 20
A coordinator dispatches four subagents in parallel. Subagents 1 and 3 return results within 10 seconds. Subagents 2 and 4 are still running at 30 seconds. The coordinator's `max_tokens` budget is 80% consumed by the results from 1 and 3 plus the pending state. What should the coordinator do?

A) Increase max_tokens to accommodate the expected additional results from subagents 2 and 4
B) Kill subagents 2 and 4 immediately to preserve the context budget and proceed with available results
C) Wait indefinitely for subagents 2 and 4 since partial results may produce incorrect synthesis
D) Continue waiting but set a timeout threshold; if 2 and 4 exceed it, record them as timed out with coverage annotations and proceed with results from 1 and 3

<details>
<summary>Answer</summary>

**D)** The correct behavior is a defined timeout with graceful degradation: allow subagents 2 and 4 a reasonable window to complete, but do not wait indefinitely. If they exceed the threshold, treat their non-response as a timeout error, apply coverage annotations to record the gap, and proceed with what is available. A is wrong because `max_tokens` is a system-level constraint that should not be increased dynamically based on subagent behavior — the architecture must function within the defined budget. B is wrong because "killing immediately" is premature — 30 seconds may be within normal bounds for complex queries, and abrupt termination loses the work already done inside those subagents. C is wrong because waiting indefinitely risks the orchestrator itself exceeding its `max_tokens` limit or stalling the pipeline without any useful output. (source: Agentic loop)

</details>

---

## Question 21
A coordinator orchestrates subagents that run in the same process with full trust. A second deployment routes the same subagents over a network API with no shared memory. Which trust-related difference affects error handling and permission design?

A) Trust level has no impact on error handling — structured error returns are required in both cases
B) Network subagents require more verbose error messages since the coordinator cannot inspect their logs
C) Same-process subagents can raise exceptions that propagate to the coordinator; network subagents cannot
D) Same-process subagents can be granted elevated permissions since the trust boundary is internal; network subagents should receive minimal scoped permissions since the channel is external and may be intercepted

<details>
<summary>Answer</summary>

**D)** Trust level directly affects permission scoping. Same-process subagents operate within the same trust boundary as the coordinator — elevated permissions are containable. Network subagents operate across a boundary that may be intercepted, spoofed, or compromised; least-privilege scoping limits blast radius if the channel or endpoint is exploited. A is wrong because trust level is directly relevant to permission design; same-process and cross-network deployments have meaningfully different attack surfaces. B is wrong because verbosity of error messages is a design choice unrelated to trust level — the coordinator should receive the same structured error schema whether the subagent is local or remote. C is wrong because the preferred pattern is to avoid exception propagation in both cases — structured error returns via tool result content is the correct approach regardless of process boundary. (source: Claude Code sub-agents)

</details>

---

## Question 22
A subagent is given the tools: `web_search`, `read_file`, `write_file`, `execute_bash`, and `send_email`. During a research task, the subagent uses `send_email` to notify stakeholders of its preliminary findings without being asked. Which principle does this violate, and what is the correct design?

A) This is an orchestration error — the coordinator should have pre-approved the email before the subagent sent it
B) This violates least privilege — give the subagent only `web_search` and `read_file` for a read-only research task
C) This violates separation of concerns — the subagent should have `send_email` but include a confirmation step before sending
D) This is acceptable behavior — subagents should proactively communicate findings to relevant parties

<details>
<summary>Answer</summary>

**B)** Least privilege means giving each agent only the tools required for its specific task. A research subagent needs `web_search` and `read_file` — it has no business need for `write_file`, `execute_bash`, or `send_email`. Removing these tools makes unintended side effects impossible by design, not merely discouraged by prompts. A is wrong because the issue is not coordinator approval of the action but the fact that the tool should not have been available to the subagent at all. C is wrong because adding a confirmation step still leaves `send_email` accessible when the task doesn't need it — the correct fix is removing the tool, not adding a gate. D is wrong because a subagent taking unsolicited external communication actions is precisely the kind of autonomous side-effect that least-privilege tool scoping prevents — "proactive" behavior that the coordinator did not authorize is a reliability failure. (source: Claude Code sub-agents)

</details>

---

## Question 23
Two subagents are deployed: one runs in the same Claude Code session as the coordinator (same-process), and one runs as a separate API-called service (cross-network). An attacker compromises the network channel to the second subagent and injects a malicious tool result. Which trust boundary design most limits the impact?

A) Require the network subagent to sign all responses with a shared secret
B) Add a coordinator-side result validator that checks all incoming tool results for malicious patterns
C) Encrypt all tool results so injected content cannot be read by the coordinator
D) Scope network subagent permissions to read-only tools so injected results cannot trigger write actions

<details>
<summary>Answer</summary>

**D)** Least-privilege permission scoping is the most direct mitigation: if the network subagent can only use read-only tools, an injected tool result cannot cause write, delete, or communication actions even if the coordinator acts on it. The blast radius is bounded by the permission scope. A is wrong because signature verification prevents tampering but does not limit what a successfully verified (or bypassed) malicious result can cause downstream. B is wrong because pattern-based validators are fragile against novel injection techniques and add complexity without addressing the root permission surface. C is wrong because encryption protects the channel but does not limit what the coordinator does with results after decryption — once decrypted, a malicious result can still trigger harmful actions. (source: Claude Code sub-agents)

</details>

---

## Question 24
A coordinator receives mixed results from six parallel subagents: three returned complete results, two returned partial results with coverage annotations, and one returned an unrecoverable error. `max_tokens` is at 70% of budget. When should the coordinator halt the orchestration rather than proceed with partial synthesis?

A) When the missing coverage would make the output fundamentally unusable for its stated purpose, or when proceeding would exceed resource constraints with unacceptable confidence
B) Whenever any subagent returns an unrecoverable error, since partial synthesis may produce misleading output
C) When more than 33% of subagents fail, since majority-complete is a reasonable threshold for quality
D) Never — the coordinator should always attempt synthesis with whatever data is available

<details>
<summary>Answer</summary>

**A)** The halt decision is purpose-driven and resource-aware: if the coverage gaps make the output unfit for its intended use or if proceeding would exhaust the token budget before synthesis can complete, halting prevents a worse outcome. B is wrong because one unrecoverable error out of six subagents does not automatically make synthesis unusable — the impact depends on what domain was lost and the output's requirements. C is wrong because a fixed percentage threshold ignores the content and importance of the missing coverage — losing 1 of 6 subagents on a peripheral topic is very different from losing the central domain. D is wrong because some coverage gaps are so fundamental that partial synthesis actively misleads the reader, making no output more honest than a misleading one. (source: Agentic loop)

</details>

---

## Question 25
A multi-agent pipeline processes financial data. The coordinator should continue with partial results in which scenario?

A) The subagent responsible for regulatory compliance data returned an unrecoverable error, and the pipeline output will be used for compliance decisions
B) The synthesis subagent itself returned an unrecoverable error after processing all collected data
C) A subagent returned results but the coordinator cannot verify they came from authorized data sources due to a trust failure
D) Two of five data collection subagents timed out, the other three succeeded, the missing domains are non-critical supplementary context, and the output will be annotated with explicit coverage gaps

<details>
<summary>Answer</summary>

**D)** Proceeding is correct when: the failed subagents covered non-critical supplementary domains, the majority of data was collected, and the output will explicitly annotate the gaps. The consumer of the output can make an informed decision with a clearly marked partial result. A is wrong because losing the compliance subagent in a compliance-decision pipeline makes the output unfit for its purpose — proceeding could cause downstream harm from false confidence. B is wrong because if synthesis itself failed, there is no output to proceed with — the coordinator must halt and report the synthesis failure. C is wrong because a trust failure in data sourcing compromises the entire result's integrity — proceeding with unverified results without halting risks propagating tainted data. (source: Agentic loop)

</details>

---

## Question 26
A research coordinator sets `stop_sequence: ["FINAL_ANSWER:"]` and `max_tokens: 4096` on each subagent call. A subagent enters an analysis loop, generating increasingly verbose intermediate reasoning. Which safeguard correctly terminates this runaway behavior?

A) The coordinator should monitor subagent output token counts and send an interrupt signal when they exceed a threshold
B) The subagent's system prompt should include an instruction to limit reasoning to 500 tokens per response
C) `max_tokens` will stop generation at 4096 tokens regardless of content; `stop_sequence` will stop generation if the subagent produces the "FINAL_ANSWER:" marker, providing a clean semantic exit point
D) The coordinator should set `temperature: 0` on the subagent to prevent verbose exploratory reasoning

<details>
<summary>Answer</summary>

**C)** `max_tokens` is a hard budget ceiling — generation stops at exactly this limit, preventing unbounded output. `stop_sequence` provides a semantic termination point — when the subagent produces its final answer marker, generation stops cleanly at a meaningful boundary. Using both together provides both a safety ceiling and a clean exit. A is wrong because there is no "interrupt signal" mechanism in the API — output monitoring is only possible after generation completes; generation itself cannot be interrupted mid-stream based on length. B is wrong because a system prompt instruction to "limit reasoning to 500 tokens" is probabilistic guidance, not a hard constraint — the model may exceed it, and the instruction itself consumes tokens. D is wrong because `temperature: 0` affects output diversity, not verbosity — a deterministic model can still generate extremely long reasoning chains. (source: Agentic loop)

</details>

---

## Question 27
A coordinator implements a runaway-agent safeguard by checking if `stop_reason == "max_tokens"` on any subagent response. When this occurs, what should the coordinator do?

A) Log the truncation, treat the response as potentially incomplete, include any partial content with an annotation, and decide whether to retry with a more constrained prompt or halt
B) Terminate the entire orchestration since a max_tokens response indicates a runaway agent
C) Silently discard the response and retry the subagent with a higher `max_tokens` value
D) Treat it as a successful completion since the subagent reached its token limit naturally

<details>
<summary>Answer</summary>

**A)** `max_tokens` truncation means the response was cut off before the model finished — it is neither a clean success nor a definitive failure. The correct handling: log the event as a potential issue, treat the content as potentially incomplete, annotate the truncation in any downstream use, and make a deliberate decision about retry with a tighter prompt versus proceeding. B is wrong because a single max_tokens truncation does not definitively indicate a runaway agent — complex queries legitimately require more output; the safeguard is logging and annotation, not automatic termination. C is wrong because silently increasing max_tokens without logging hides the truncation event from downstream reasoning and may cause the same overrun behavior with a higher ceiling. D is wrong because reaching max_tokens is not a "natural completion" — `end_turn` indicates natural completion; `max_tokens` indicates forced interruption of an incomplete generation. (source: Agentic loop)

</details>

---

## Question 28
A coordinator needs to implement a safeguard against subagents entering infinite tool-call loops. Which combination of `stop_sequence` and `max_tokens` configuration best addresses this?

A) Set `max_tokens: 100000` to ensure the agent always has enough room and rely on `stop_sequence` for loop detection
B) Set `max_tokens` to a value appropriate for the expected task scope and add a `stop_sequence` for the final answer marker; additionally track iteration count in the coordinator and halt if the subagent requests more than N tool calls
C) Rely solely on `stop_sequence: ["DONE"]` since infinite loops only happen if the agent never generates this token
D) Set `max_tokens: 100` to force early termination and prevent loops entirely

<details>
<summary>Answer</summary>

**B)** Defense-in-depth: `max_tokens` bounds the token budget per generation, `stop_sequence` provides a semantic exit, and a coordinator-side iteration count caps the number of tool-call round trips. Each layer addresses a different runaway scenario: excessive output (max_tokens), incomplete termination signal (stop_sequence), and excessive tool round trips (iteration count). A is wrong because a very high `max_tokens` provides almost no protection against runaway generation — it defeats the purpose of the budget safeguard. C is wrong because relying solely on `stop_sequence` fails whenever the model enters a loop that never produces the sequence — the model could loop indefinitely on tool calls without ever generating "DONE". D is wrong because `max_tokens: 100` is far too low for legitimate complex tasks and would truncate valid responses before completion. (source: Agentic loop)

</details>

---

## Question 29
A coordinator must decide whether to halt orchestration or continue with partial results after a subagent returns an unrecoverable error for the "economic impact" domain of a policy research report. The client has specified this report must address all five policy domains. Which is the correct decision?

A) Halt orchestration and report to the client that the requested deliverable cannot be completed as specified, identifying the missing domain and asking for guidance
B) Continue synthesis and note the gap in a footnote, since four of five domains are complete
C) Replace the "economic impact" domain with available data from adjacent domains to maintain five sections
D) Proceed with synthesis and omit the economic impact section from the table of contents

<details>
<summary>Answer</summary>

**A)** When a client requirement explicitly specifies full coverage and a critical domain is irrecoverably lost, proceeding produces output that does not meet the specification — continuing creates false confidence. The correct action is to halt and surface the gap clearly so the client can decide: accept partial output, source alternative data, or extend the timeline. B is wrong because a footnote does not satisfy a client requirement for complete domain coverage — delivering a four-domain report when five were promised without explicit client acknowledgment is a deliverable failure. C is wrong because substituting adjacent domain data misrepresents the content — the economic impact section would contain non-economic content under a misleading header. D is wrong because omitting the section from the table of contents without notification is equivalent to silent failure — the client cannot see what was dropped. (source: Agentic loop)

</details>

---

## Question 30
A multi-agent research system's coordinator receives this from a subagent after processing 10 documents: `{"processed": 10, "successful": 7, "failed": 3, "failures": [{"doc": "report_A.pdf", "type": "parse_error", "recoverable": false}, {"doc": "brief_B.docx", "type": "access_denied", "recoverable": false}, {"doc": "data_C.csv", "type": "rate_limit", "recoverable": true, "retry_after": 20}]}`. What is the correct coordinator response?

A) Discard the entire batch and resubmit all 10 documents to a fresh subagent instance
B) Halt the pipeline since multiple failures indicate a systemic problem with the subagent
C) Proceed with results from the 7 successful documents; mark report_A and brief_B as permanent coverage gaps; schedule a retry for data_C after 20 seconds
D) Retry all three failed documents before proceeding since 30% failure is too high for reliable synthesis

<details>
<summary>Answer</summary>

**C)** The structured error payload provides exactly the information needed for targeted recovery. `report_A` (parse error, not recoverable) and `brief_B` (access denied, not recoverable) should be annotated as permanent gaps — retrying would fail the same way. `data_C` (rate limit, recoverable, retry_after: 20) is a clear candidate for a timed retry. The 7 successful results should proceed immediately. A is wrong because discarding all 10 documents including the 7 successful ones is massively wasteful — the structured error report is exactly the mechanism that makes targeted recovery possible. B is wrong because three heterogeneous failures (parse error, access denial, rate limit) on different documents indicate individual document issues, not a systemic subagent failure — 70% success rate with diverse failure types is not evidence of systemic breakdown. D is wrong because applying a uniform retry to all three ignores the `recoverable` flags — retrying `report_A` and `brief_B` will fail again for the same reasons, wasting time and resources. (source: Tool use)

</details>

---
