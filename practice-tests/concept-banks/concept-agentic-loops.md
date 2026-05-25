# Agentic Loops — Question Bank

## Question 1
You are building a customer support agent. Your agentic loop currently checks if the assistant's response contains the phrase "I've completed the task" to decide when to stop iterating. During testing, the agent sometimes generates this phrase mid-conversation while still intending to call additional tools. What should you change?

A) Add additional termination phrases like \"No additional action needed\" to make detection more robust
B) Check stop_reason in the API response: continue when it equals \"tool_use\" and terminate when it equals \"end_turn\"
C) Set a maximum iteration count and stop after that many loops regardless of the response content
D) Parse the assistant's response for tool call JSON to determine if more tools need to be invoked

<details>
<summary>Answer</summary>

**B)** stop_reason is the API-provided, deterministic signal for loop control — "tool_use" means the model wants to invoke a tool, "end_turn" means it has finished. Natural language parsing is unreliable because the model may generate completion-sounding phrases while still mid-task. A is wrong because adding more termination phrases compounds the same unreliable heuristic — the model can produce any phrase in any context, so no phrase list is safe. C is wrong because an iteration cap is only a safety fallback, not a primary stopping mechanism — using it as the primary condition causes premature termination on legitimate long tasks. D is wrong because parsing tool call JSON in response text is another form of natural language parsing and fragile against model output variation. (source: Agentic loop)

</details>

---

## Question 2
Your agentic loop processes tool results but does not append them to the conversation history before sending the next request. The agent appears to "forget" what tools returned and re-calls the same tools repeatedly. What is the root cause?

A) The model's context window is too small to hold the tool results
B) Tool results must be appended to the conversation history so the model can reason about them in the next iteration
C) The model needs a system prompt instruction telling it not to repeat tool calls
D) You need to implement a deduplication layer that prevents the same tool from being called twice

<details>
<summary>Answer</summary>

**B)** The conversation history is the model's only memory between API calls — tool results not appended to history are invisible to the model in the next iteration, causing it to re-invoke the same tools. A is wrong because the issue is absence of results in the history, not window size — even a large context window cannot display data that was never appended. C is wrong because a system prompt instruction cannot compensate for data the model literally cannot see; the model will still call tools again because no prior results exist in its context. D is wrong because deduplication is a band-aid that hides the root cause — the loop should append results correctly rather than prevent legitimate re-calls. (source: Agentic loop)

</details>

---

## Question 3
A developer implements an agentic loop with max_iterations = 5 as the primary stopping condition. The agent frequently hits this limit mid-task, producing incomplete responses. The developer's fix is to increase the limit to 20. What is the better approach?

A) Use stop_reason == \"end_turn\" as the primary termination condition, with the iteration cap as a safety fallback only
B) Set max_iterations = 50 to ensure the agent always has enough room to complete
C) Remove the iteration cap entirely and let the agent run until it finishes naturally
D) Add a timer-based cutoff (e.g., 60 seconds) instead of an iteration count

<details>
<summary>Answer</summary>

**A)** stop_reason == "end_turn" is the authoritative signal that the model has finished; the iteration cap should only exist as a runaway-loop safeguard. Using the cap as the primary mechanism conflates "ran out of budget" with "finished the task." B is wrong because increasing the cap merely pushes the problem further — the root cause (wrong primary condition) is unchanged and the agent can still terminate mid-task on complex requests. C is wrong because removing the cap entirely creates unbounded runaway risk — loops with tool errors, bad prompts, or infinite cycles would never terminate. D is wrong because a timer-based cutoff is unrelated to task completion state and can terminate the loop either too early (on slow tools) or never (on fast but infinite loops). (source: Agentic loop)

</details>

---

## Question 4
In your agentic loop, after the model returns a response with stop_reason: "tool_use", you execute the requested tool and get a result. What should happen next?

A) Send a new API request with only the tool result as the user message
B) Append the assistant's response (with the tool call) and the tool result to the conversation history, then send the full updated history in the next API request
C) Parse the tool result and include a summary in the next system prompt update
D) Store the tool result in a database and include a reference ID in the next message

<details>
<summary>Answer</summary>

**B)** Both the assistant's tool_use message and the tool_result message must be appended to the conversation history and sent in the next request — this gives the model full context to reason about the result and decide what to do next. A is wrong because sending only the tool result omits the assistant's prior tool_use block, which is required by the API message schema — the model also loses the conversational context of what question it was answering. C is wrong because the system prompt is for persistent instructions, not for passing dynamic tool results; summarizing tool data there distorts its purpose and discards fidelity. D is wrong because an external database reference provides no reasoning-relevant content — the model needs the actual result in its context, not an opaque pointer. (source: Agentic loop)

</details>

---

## Question 5
You notice your agentic loop terminates when the assistant message contains text content alongside a tool call. The code checks if response.content[0].type == "text": break. Why is this incorrect?

A) The content array can contain both text blocks and tool_use blocks in the same response. The model often explains its reasoning before or after requesting a tool call
B) Text content is only present in error responses, so this check is correct for normal flow
C) The content array always has exactly one element, so checking the first element is fine
D) Tool calls are never mixed with text content in the same response

<details>
<summary>Answer</summary>

**A)** A single assistant response can contain both text blocks and tool_use blocks in the same content array — the model frequently adds reasoning text alongside tool invocations. The termination check must use stop_reason, not the type of the first content block. B is wrong because text content is the normal output format for assistant replies; it is present in both tool-calling and final responses, not exclusively in errors. C is wrong because the content array can have multiple elements — checking only the first element and ignoring the rest misses any tool_use blocks that appear after the text block. D is wrong because mixed text and tool_use content is an explicitly documented and common pattern in Claude's API responses. (source: Agentic loop)

</details>

---

## Question 6
Your customer support agent uses an agentic loop. In production, you observe that the agent sometimes enters an infinite loop, calling the same two tools alternately without making progress. What is the best mitigation?

A) Parse each tool result for the word \"error\" and terminate the loop if detected
B) Maintain a reasonable iteration safety cap as a fallback and monitor for repeated identical tool calls as a signal to investigate prompt or tool design issues
C) After each tool call, ask the model \"Are you done?\" and terminate if it says yes
D) Limit each tool to being called only once per session

<details>
<summary>Answer</summary>

**B)** An iteration safety cap prevents runaway loops, and monitoring for repeated identical tool calls surfaces root-cause issues in prompt clarity or tool description quality. A is wrong because parsing for the word "error" is unreliable natural language detection — the word may appear in valid results or be absent in real errors, and it does not catch non-error infinite cycles. C is wrong because asking "Are you done?" inserts unnecessary conversational turns, increasing token cost and latency, and the model's yes/no answer is itself an unreliable signal. D is wrong because legitimate workflows may need to call the same tool multiple times with different parameters — a per-session call limit would break valid multi-step queries. (source: Agentic loop)

</details>

---

## Question 7
What distinguishes model-driven decision-making in an agentic loop from a pre-configured decision tree?

A) Model-driven decision-making is slower but more accurate than decision trees
B) In model-driven loops, Claude reasons about which tool to call next based on the current context, rather than following a fixed sequence of tool calls
C) Decision trees use the API while model-driven approaches use local inference
D) Model-driven approaches require fewer tools to be defined

<details>
<summary>Answer</summary>

**B)** In model-driven agentic loops, Claude dynamically evaluates the current context and decides which tool to invoke next, enabling adaptation to novel situations not anticipated at design time. A is wrong because speed versus accuracy is not the defining distinction — the key difference is dynamic versus fixed sequencing, and neither approach is universally more accurate. C is wrong because both decision trees and model-driven agents can use the API or local inference; the distinction is about logic control, not the inference location. D is wrong because the number of tools defined is independent of whether control flow is model-driven or hard-coded — a decision tree can have many branches with many tools, and a model-driven loop may use few. (source: Agentic loop)

</details>

---

## Question 8
You are designing an agentic loop for a billing dispute agent. The agent must: (1) look up the customer, (2) retrieve the disputed charge, (3) check the refund policy, and (4) either process the refund or escalate. A junior developer suggests hard-coding this sequence. What is the tradeoff?

A) Hard-coding is always better because it guarantees the correct order
B) Hard-coding ensures the sequence but loses the model's ability to adapt. A hybrid approach using programmatic prerequisites for critical steps and model-driven logic for adaptive steps is often better
C) Model-driven is always better because it is more flexible
D) There is no difference — the model will follow the same sequence either way

<details>
<summary>Answer</summary>

**B)** Hard-coding enforces order predictably but removes the model's ability to handle edge cases, alternate paths, or user-initiated context shifts; a hybrid approach uses programmatic enforcement only for non-negotiable prerequisites while allowing model-driven reasoning for adaptive steps. A is wrong because hard-coding is not always better — it fails to handle legitimate deviations such as a customer volunteering their order number before being asked, or an edge case requiring a step to be skipped. C is wrong because model-driven control is not always better either — for high-stakes prerequisites like identity verification before a financial action, programmatic enforcement provides deterministic safety guarantees the model cannot. D is wrong because the sequence the model follows is contextually determined, not guaranteed to match the hard-coded order — the model may call steps out of order if context cues suggest it. (source: Agentic loop)

</details>

---

## Question 9
Your agentic loop implementation sends the API request, receives a response, and checks stop_reason. The response has stop_reason: "max_tokens". What does this indicate and how should you handle it?

A) The model finished its response normally. Terminate the loop
B) The model's response was truncated because it hit the max_tokens limit. Continue the conversation or increase max_tokens
C) The model encountered an error. Retry the same request
D) The model wants to call a tool but ran out of space to specify which one. Terminate and report an error

<details>
<summary>Answer</summary>

**B)** stop_reason "max_tokens" means the output was cut off before the model finished — the response is incomplete and may contain a partial tool call or truncated reasoning. The correct action is to either increase max_tokens or send a continuation request. A is wrong because "end_turn" is the signal for normal completion — "max_tokens" specifically means the response was cut short, not finished. C is wrong because this is not an API error requiring a retry of the same request — retrying without changes will produce the same truncated output. D is wrong because "max_tokens" is not a special tool-related state — it simply means the response hit the output token budget, and the correct fix is adjusting that budget or continuing. (source: Agentic loop)

</details>

---

## Question 10
Which of the following is the correct agentic loop control flow?

A) Send request -> Check if response contains tool JSON -> Execute tool -> Loop until no tool JSON found
B) Send request -> Check stop_reason -> If \"tool_use\": execute tool, append results to history, send next request -> If \"end_turn\": return final response
C) Send request -> Execute all tools defined in the system -> Append results -> Send next request -> Check for \"done\" in response text
D) Send request -> If response has text content, return it -> If response has tool content, execute and loop

<details>
<summary>Answer</summary>

**B)** The correct loop uses stop_reason as the decision point: "tool_use" triggers tool execution with full history append and re-request; "end_turn" signals completion. A is wrong because checking for tool JSON in the response body is unreliable natural language parsing — the model may discuss tool calls in text without actually invoking them, and the stop_reason is the authoritative signal. C is wrong because executing all tools defined in the system regardless of what the model requested is not how the API works — only the specific tool_use blocks in the response should be executed. D is wrong because text content and tool content can coexist in the same response — treating any text as a terminal condition causes premature loop exit. (source: Agentic loop)

</details>

---

## Question 11
Your agentic loop appends every message to the conversation history without limit. After 15 iterations, the token count approaches the model's context window. What is the best approach to manage this?

A) Stop appending old messages once the token limit is reached — the model only needs recent context
B) Implement progressive summarization: summarize earlier turns while keeping recent full context, and trim the oldest messages when needed
C) Reduce max_tokens to force shorter responses from the model, conserving context for more iterations
D) Reset the conversation every 10 turns and start fresh, passing only the original system prompt

<details>
<summary>Answer</summary>

**B)** Progressive summarization condenses older turns into compact summaries that preserve key information while freeing context space — the model retains awareness of earlier work without raw token cost. A is wrong because silently dropping old messages without summarization causes the model to lose critical information established earlier in the task, such as discovered facts or prior decisions. C is wrong because reducing max_tokens constrains the model's output quality and may truncate tool call specifications — it does not reduce input token growth and is the wrong lever. D is wrong because resetting the conversation discards all accumulated context including tool results, discovered data, and established state, forcing the model to start from scratch on work that was already completed. (source: Agentic loop)

</details>

---

## Question 12
A single assistant response contains two tool_use blocks and a text block explaining the reasoning. Your loop iterates per API call. What is the correct way to process this response?

A) Only execute the first tool_use block, since the text block indicates the model is still reasoning and not ready for execution
B) Execute all tool_use blocks in the response, capture each result, append them all to history, then send the next API request
C) Split the response into separate API calls — one per tool_use block — to give the model space to reason between them
D) Ignore the tool_use blocks and wait for a response with only tool_use blocks and no text content

<details>
<summary>Answer</summary>

**B)** When stop_reason is "tool_use", all tool_use blocks in the response must be executed — the model issued them as a coordinated batch, and all results must be returned together. A is wrong because the text block is the model's reasoning narration, not a signal of incompletion — its presence alongside tool_use blocks is normal and does not mean only partial execution is intended. C is wrong because splitting into separate API calls breaks the response structure, introduces artificial reasoning turns the model did not request, and wastes tokens re-establishing context. D is wrong because waiting for a "pure" tool_use response ignores legitimate batch tool calls and would stall the loop indefinitely. (source: Agentic loop)

</details>

---

## Question 13
Your agent calls a tool that returns an error. How should the tool result be structured to help the model recover effectively in the next loop iteration?

A) Return an empty result with no error indication — the model will detect the issue from context
B) Return the error with isError: true, an errorCategory field, and a human-readable description of what went wrong
C) Re-throw the error as an exception in your agent code and crash the agentic loop
D) Return a generic string like \"Error occurred\" and let the model decide how to proceed

<details>
<summary>Answer</summary>

**B)** Structured error results with isError: true, a categorized error type, and a descriptive message give the model actionable signal — it can reason about whether to retry, choose a different tool, or escalate. A is wrong because an empty result provides no signal; the model cannot distinguish between "the tool succeeded with no data" and "the tool failed," so it cannot take corrective action. C is wrong because crashing the loop on tool errors discards the model's ability to self-correct — tool errors are expected failure modes that a well-designed loop should handle gracefully. D is wrong because a generic "Error occurred" string gives the model no information about error category, cause, or recovery path, reducing it to guessing rather than reasoning. (source: Agentic loop)

</details>

---

## Question 14
Your agentic loop calls a tool that takes 30 seconds to respond. During this time, the user sends a follow-up message. What is the correct way to handle this?

A) Discard the slow tool result and respond to the user's new message immediately
B) Process the tool result when it arrives, append it to history along with the user's follow-up, and let the model handle the combined context in the next request
C) Block the user from sending messages until the tool completes
D) Start a separate agentic loop for the new message and merge results later

<details>
<summary>Answer</summary>

**B)** Appending both the late tool result and the follow-up message to history gives the model full context in the next iteration — it can address the follow-up while incorporating the tool's findings. A is wrong because discarding a completed tool result wastes the work already done and loses data that may be directly relevant to the user's follow-up question. C is wrong because blocking the user degrades UX with no technical benefit — the server-side processing continues regardless of whether the user can type. D is wrong because separate loops for related messages create coordination complexity, risk conflicting actions, and require merging logic that is harder to reason about than a unified history. (source: Agentic loop)

</details>

---

## Question 15
Your refund processing agent must NEVER process a refund over $500 without manager approval. The agentic loop has a check_refund_policy tool and a process_refund tool. What is the safest approach?

A) Add a system prompt instruction: \"Never process refunds over $500 without manager approval\" and rely on the model to follow it
B) Use a PostToolUse hook in the agentic loop that intercepts process_refund calls, checks the amount, and blocks + redirects to escalation if over $500
C) Add the rule to the process_refund tool description and rely on the model to read it before calling
D) Remove the process_refund tool entirely and have the model only recommend actions for humans

<details>
<summary>Answer</summary>

**B)** A PostToolUse hook provides programmatic, deterministic enforcement — the check runs in code regardless of model behavior, making it impossible for the rule to be bypassed due to prompt drift or edge-case reasoning. A is wrong because system prompt instructions are probabilistic — the model follows them as guidelines, not hard constraints, and can produce non-compliant outputs under unusual phrasing or adversarial inputs. C is wrong because tool descriptions are also probabilistic guidance; the model may overlook or misapply them, especially when tool descriptions are long or the instruction is buried. D is wrong because removing the tool eliminates agent capability unnecessarily — the correct approach is to allow the tool with a hard programmatic gate, not to remove it entirely. (source: Agentic loop)

</details>

---

## Question 16
In your agentic loop, a tool returns multiple valid results. The model needs to pick one and proceed. However, the loop keeps calling the same discovery tool instead of moving forward. What is most likely wrong?

A) The iteration cap is too low — increase it to give the model more room
B) The tool results don't provide enough distinguishing information for the model to make a decision. Add structured fields that help the model compare and choose
C) The model is confused by the large context window — reduce max_tokens
D) The tool name is ambiguous — rename it to something more specific

<details>
<summary>Answer</summary>

**B)** When the model repeatedly calls a discovery tool without advancing, it cannot find sufficient signal in the results to commit to a choice — adding structured comparative fields such as confidence scores, match quality, or priority flags gives the model the information needed to decide. A is wrong because increasing the iteration cap only extends the loop's ability to spin — it does not supply the missing decision signal, so the model will continue re-calling the tool. C is wrong because reducing max_tokens constrains output space and has no effect on the model's ability to evaluate tool result content; context window confusion is not the mechanism here. D is wrong because renaming a tool changes its discovery label but does not change the result structure — the model's indecision stems from result content, not tool naming. (source: Agentic loop)

</details>

---

## Question 17
You are implementing an agentic loop for a research assistant. The assistant must search multiple databases, compare results, and synthesize findings. What is the optimal tool execution strategy?

A) Define one tool per database and let the model call them sequentially, analyzing each result before the next call
B) Define a single search_all tool that queries all databases in parallel and returns consolidated results in one response
C) Hard-code the sequence: always search database A, then B, then C in order
D) Let the model call any tool it wants but limit each database to one call per session to save tokens

<details>
<summary>Answer</summary>

**B)** A search_all tool that parallelizes queries and returns consolidated results reduces loop iterations, eliminates intermediate reasoning turns over partial data, and gives the model a complete picture for synthesis in a single step. A is wrong because sequential per-database calls multiply the number of iterations and cause the model to generate intermediate reasoning about incomplete results — this wastes tokens and slows task completion. C is wrong because hard-coding the search sequence removes the model's ability to adapt — if database A is unavailable or irrelevant, the loop cannot skip or reorder it. D is wrong because a per-session call limit arbitrarily restricts legitimate re-queries, such as refining a search with different parameters after seeing initial results. (source: Agentic loop)

</details>

---

## Question 18
Your agentic loop processes user requests by calling tools. After 3 iterations, you notice the response quality degrades — the model starts repeating itself and making simple mistakes. What is the likely cause?

A) The model has reached its maximum intelligence level for this session — restart the conversation
B) Context degradation from accumulated tool outputs and conversation history is overwhelming relevant information. Consider progressive summarization or trimming verbose tool results
C) The model is tired and needs a cooldown period between requests
D) The max_tokens setting is too low — increase it to give the model more space per iteration

<details>
<summary>Answer</summary>

**B)** As accumulated tool outputs and conversation history grow, the signal-to-noise ratio in the context decreases — the model must search through more content to find relevant information, causing reasoning errors. Progressive summarization and trimming verbose tool results restore signal clarity. A is wrong because there is no "maximum intelligence level" per session — the model's capabilities are constant, but its performance degrades when context becomes cluttered with irrelevant or redundant content. C is wrong because the model has no fatigue mechanism — degradation is a function of context quality, not time elapsed between requests. D is wrong because max_tokens controls output length, not the model's ability to reason over its input — increasing it will not reduce context clutter or improve comprehension of a noisy history. (source: Agentic loop)

</details>

---

## Question 19
You configure tool_choice: "auto" in your agentic loop. In testing, the model sometimes returns end_turn without calling any tool, even though the user clearly expected a tool-based response. What is the best fix?

A) Switch to tool_choice: \"any\" to guarantee a tool is called in each iteration
B) Improve the system prompt and tool descriptions to make it clearer when each tool should be used. The model with \"auto\" decides based on context and descriptions
C) Add a tool that always returns a result, ensuring at least one tool call per turn
D) Ignore it — the model knows best when to call tools

<details>
<summary>Answer</summary>

**B)** With tool_choice: "auto", the model's decision is driven by context quality and tool description clarity — if it declines to call a tool when one is needed, the descriptions or system prompt lack sufficient guidance. A is wrong because tool_choice: "any" forces a tool call every iteration, including turns where the correct behavior is to respond in text — this wastes tokens on unnecessary tool invocations and can break conversational flows. C is wrong because adding a dummy tool that always returns a result manipulates the tool-calling mechanism rather than fixing the underlying signal quality, and the always-called tool consumes tokens without purpose. D is wrong because "the model knows best" is only true when it has adequate information — if the descriptions are unclear, the model makes poorly informed decisions that the developer is responsible for correcting. (source: Agentic loop)

</details>

---

## Question 20
Your agentic loop implementation runs in production. A bug causes the same tool result to be appended to the conversation history twice. What impact does this have?

A) No impact — the model ignores duplicate content
B) The model may interpret the duplicate as two separate, corroborating results, leading to overconfidence or repeated reasoning about the same data. Token costs also increase unnecessarily
C) The API automatically deduplicates content blocks before processing
D) The model immediately detects the error and requests corrected data

<details>
<summary>Answer</summary>

**B)** Duplicate tool results inflate token costs and can bias the model into treating identical data as independent corroboration, increasing confidence in results that should be evaluated once. A is wrong because the model processes all content in its context — it does not identify or suppress duplicates, and the repeated data actively influences its reasoning. C is wrong because the API passes the conversation history as provided — there is no deduplication layer; the responsibility for correct history management lies entirely with the caller. D is wrong because the model has no mechanism to detect that a result appeared twice or to issue a structured correction request — it simply reasons over all content it receives. (source: Agentic loop)

</details>

---

## Question 21
Your agentic loop handles a customer refund workflow. The customer asks "Can you check my order status?" The agent calls lookup_order and returns the status. The customer then says "Actually, I want a refund." How should the loop handle this shift in context?

A) Reset the conversation and start fresh — the refund flow needs clean context
B) Continue the existing loop — the conversation history already contains the order lookup result, which is relevant to processing the refund
C) Parse the user's message for keywords and route to a different agent
D) Ignore the refund request since it wasn't the original intent

<details>
<summary>Answer</summary>

**B)** The conversation history already contains the order lookup result, which is directly relevant to the refund — continuing the loop avoids redundant tool calls and leverages already-gathered context. A is wrong because resetting the conversation discards the order data that was just retrieved, forcing a redundant lookup_order call and increasing latency and token cost for no benefit. C is wrong because routing to a different agent on a keyword match introduces unnecessary complexity and forfeits the existing context — the current loop has everything needed to handle the refund. D is wrong because the user's follow-up is a legitimate in-session intent shift that the agentic loop is designed to accommodate through its conversation history. (source: Agentic loop)

</details>

---

## Question 22
You implement an agentic loop that uses extended thinking (adaptive mode). After each tool call, you want Claude to reason about the result before deciding the next action. What configuration is needed?

A) No special configuration — adaptive thinking automatically enables interleaved thinking, allowing reasoning between tool calls
B) You must use tool_choice: \"any\" to force Claude to think between tool calls
C) Extended thinking only works before the first tool call — you cannot reason between subsequent calls
D) You need to add a separate \"think\" tool that the model calls to indicate it is reasoning

<details>
<summary>Answer</summary>

**A)** Adaptive thinking mode automatically enables interleaved thinking, which allows Claude to produce reasoning blocks between tool calls without any additional configuration — this is the intended mechanism for multi-step agentic reasoning. B is wrong because tool_choice: "any" controls whether tools must be called, not whether thinking is interleaved — it would force a tool call every turn, which is unrelated to enabling reasoning between calls. C is wrong because interleaved thinking is specifically designed to work throughout multi-step loops, not just before the first tool call — reasoning between calls is a core capability of adaptive thinking mode. D is wrong because adding a "think" tool is a workaround that consumes tool slots, creates unnecessary API overhead, and is redundant given that adaptive thinking already provides native interleaved reasoning. (source: Extended thinking)

</details>

---

## Question 23
Your agent uses fork_session to create a sub-agent that processes a subtask. The sub-agent completes its work and returns results. What happens to the conversation history of the sub-agent's session?

A) The sub-agent's session history is automatically merged into the parent session
B) The sub-agent's session is independent — you must explicitly pass the relevant results back to the parent session as context
C) The sub-agent's session replaces the parent session entirely
D) Both sessions share the same history — any changes in one reflect in the other

<details>
<summary>Answer</summary>

**B)** fork_session creates an isolated session that inherits the parent's context at fork time but diverges independently — the sub-agent's subsequent history stays in its own session and must be explicitly extracted and passed back to the parent. A is wrong because automatic history merging does not occur — if it did, sub-agent intermediate reasoning and tool calls would pollute the parent's context, creating noise and potentially conflicting with the parent's own reasoning. C is wrong because the sub-agent's session runs in parallel alongside the parent session, not as a replacement — the parent continues to exist and coordinate. D is wrong because the sessions are intentionally isolated after the fork point; shared history would defeat the purpose of forking, which is to give the sub-agent an independent workspace. (source: Agentic loop)

</details>

---

## Question 24
In your agentic loop, the model calls tool A with parameter X, then in the next iteration calls tool A again with parameter Y. Both calls succeed. How should the loop process this?

A) Block the second call — calling the same tool twice indicates a bug
B) Execute both calls normally and append both results to history. The model may legitimately need to call the same tool with different parameters
C) Merge the two calls into one with both parameters and return a combined result
D) Cache the first result and return it for the second call without executing again

<details>
<summary>Answer</summary>

**B)** Calling the same tool with different parameters is a legitimate and common pattern — for example, querying the same database for two different customer IDs. Each call should execute independently and both results appended to history. A is wrong because same-tool repetition is not a bug indicator — the correct bug signal is identical tool calls with identical parameters in a loop, not different-parameter calls across iterations. C is wrong because merging calls with different parameters changes the query semantics — the model issued two distinct requests and expects two distinct results, not a combined response. D is wrong because caching tool results by tool name ignores parameter differences — returning a stale result for a different parameter input corrupts the model's data and produces incorrect downstream reasoning. (source: Agentic loop)

</details>

---

## Question 25
Your agentic loop sends requests with thinking: {type: "adaptive", display: "omitted"} to save latency. You notice the model makes more errors on multi-step tasks compared to display: "summarized". What is the likely cause?

A) Display mode has no effect on reasoning quality — the errors are unrelated to the display setting
B) The model is running out of token budget with omitted display — increase max_tokens
C) Omitted display disables interleaved thinking, so the model cannot reason between tool calls
D) The model thinks less carefully because it knows its reasoning won't be visible to the user

<details>
<summary>Answer</summary>

**A)** display: "omitted" only controls what is streamed to the client — the model's internal thinking depth, quality, and interleaved reasoning operate identically regardless of display mode. The observed errors are caused by something else such as ambiguous tool descriptions, insufficient context, or tool design issues. B is wrong because display mode does not affect token budget consumption for thinking — the model thinks the same amount; only the streaming output is suppressed, not the reasoning itself. C is wrong because interleaved thinking is controlled by the thinking type (adaptive/enabled), not the display setting — omitted display does not disable or reduce interleaved reasoning. D is wrong because the model has no awareness of or behavioral change based on whether its thinking will be visible; its reasoning process is independent of the display configuration. (source: Extended thinking)

</details>

---

## Question 26
Your agentic loop detects that the user's question can be answered by running two independent tool calls. The model returns both tool_use blocks in a single response. How should the loop execute these?

A) Execute the first tool, wait for the result, then execute the second — sequential execution is safer
B) Execute both tools in parallel since they are independent, collect both results, then append them together to history
C) Only execute the first tool and ignore the second — the model will re-request it if needed
D) Split this into two separate API requests — one per tool call

<details>
<summary>Answer</summary>

**B)** Independent tool calls returned in a single response should be executed in parallel — this minimizes latency and matches the model's intent in issuing them as a batch. Both results are then appended together before the next API request. A is wrong because sequential execution of independent tools doubles the wall-clock latency for no benefit — the "safety" argument does not apply when the tools have no data dependency on each other. C is wrong because ignoring a tool_use block in the model's response means returning an incomplete set of results — the model will not know its second request was silently dropped and will reason incorrectly from partial data. D is wrong because splitting into separate API requests adds unnecessary round-trips, re-establishes context twice at token cost, and misrepresents the model's batched intent. (source: Agentic loop)

</details>

---

## Question 27
Your agentic loop has been running for 20 iterations. The conversation history is now very large. You notice the API response time has increased significantly. What is the primary cause?

A) The model gets slower the longer it thinks — this is expected behavior
B) The input token count has grown with each iteration, increasing processing time per request. Consider progressive summarization or trimming older context
C) The API rate-limits based on total session duration — you need to increase your rate limit
D) The tool execution time accumulates — add caching to reduce tool call latency

<details>
<summary>Answer</summary>

**B)** API processing time scales with input token count — each iteration appends more content to the history, and the growing input directly increases time-to-first-token. Progressive summarization of earlier turns and trimming verbose tool outputs controls this growth. A is wrong because the model does not slow down over session time — processing time is a function of input size per request, not cumulative session duration. C is wrong because API rate limits operate on requests-per-minute or tokens-per-minute, not total session length — the slowdown is caused by larger input sizes, not rate limiting. D is wrong because tool execution happens outside the API call — tool latency does not affect API response time, which is measured from the moment the API receives its input to when it begins returning output. (source: Agentic loop)

</details>

---

## Question 28
You implement a validation loop: the model extracts data, a validator checks it, and if invalid, the error is appended for the model to retry. After 3 retries on the same field, the model still produces invalid data. What should you do?

A) Increase the retry limit to 10 — the model just needs more attempts to get it right
B) After a configurable max retries (e.g., 3), terminate the loop and escalate or use fallback logic. Persistent failures indicate the task may need a different approach
C) Append the error more forcefully — use ALL CAPS in the error message to signal urgency
D) Clear the conversation history and restart the extraction from scratch

<details>
<summary>Answer</summary>

**B)** When the model fails the same validation repeatedly, continuing to retry with the same approach is unlikely to succeed — the task itself may be ambiguous, the schema may be malformed, or the source data may be invalid. Escalation or fallback logic is the correct response to persistent failure. A is wrong because increasing the retry limit to 10 extends a failing approach — if 3 attempts with the same prompt and error feedback did not work, additional retries with the same strategy will not fix the underlying issue. C is wrong because formatting error messages in ALL CAPS is not a documented or reliable mechanism for improving model compliance — the model does not interpret typographic emphasis as urgency signals. D is wrong because clearing history removes the accumulated context about what was tried and why it failed, which is precisely the information the model needs to take a different approach if retried. (source: Agentic loop)

</details>

---

## Question 29
Your agentic loop processes a user request by calling search_documents, extract_passages, and summarize_results. The model calls all three tools across separate iterations. On the second attempt, the model calls extract_passages before search_documents completes. What happens?

A) The response is rejected by the API — tools must be called in the order they appear in the tools array
B) The API processes the request, but the model is working without search results. The loop should include validation that prerequisite tools complete before dependent tools are called
C) The model knows best — execute extract_passages and it will work regardless
D) The API reorders the tool calls to respect dependencies automatically

<details>
<summary>Answer</summary>

**B)** The API executes whatever tool call the model requests without enforcing dependencies — if extract_passages is called before search_documents completes, it runs against missing or stale data. The loop or the tool itself must enforce prerequisite ordering. A is wrong because the API does not validate tool call ordering against any declared dependency graph — the tools array defines available tools, not required sequencing. C is wrong because extract_passages operating without prior search results will either fail or produce incorrect output — the model cannot overcome a data dependency violation at execution time. D is wrong because the API has no knowledge of semantic dependencies between tools and performs no reordering — dependency management is entirely the responsibility of the calling application. (source: Agentic loop)

</details>

---

## Question 30
Your agentic loop is designed to process a batch of 50 customer records. After processing 30, the response quality drops noticeably. The remaining 20 records have more errors. What is the most effective mitigation?

A) Use progressive summarization to condense the first 30 results into a summary, keeping only recent full context for the remaining items
B) Reduce the batch size to 10 and loop through smaller batches
C) Increase max_tokens to give the model more room for the remaining records
D) Clear the history after each record and start fresh — the model doesn't need historical context for independent records

<details>
<summary>Answer</summary>

**A)** Progressive summarization condenses the first 30 results into a compact aggregate summary — preserving patterns, error rates, and key findings — while keeping recent records at full fidelity. This reduces context clutter while maintaining awareness of overall batch progress. B is wrong because reducing batch size to 10 changes the task structure rather than fixing the context management problem — the same degradation would occur after processing the first batch, and the approach multiplies coordination overhead. C is wrong because max_tokens controls output length per response, not the model's ability to reason over a growing input history — the degradation is caused by input context noise, not output space constraints. D is wrong because clearing history after each record discards patterns and aggregate signals discovered earlier in the batch — for example, anomalous charge types seen in records 1–10 that are relevant to evaluating record 31. (source: Agentic loop)

</details>

---
