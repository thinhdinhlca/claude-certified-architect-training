# Tool Use & Extended Thinking — Question Bank

## Question 1
A junior engineer defines a tool with name: 'get-stock-price!' and input_schema with required: []. The description says 'Gets stock price.' On first API call, the model calls the tool with no arguments. What is the most likely root cause?

A) The model doesn't understand the tool name because of the exclamation mark, so it ignores the schema requirements
B) The description is too brief - the model doesn't know a ticker parameter is needed, so it omits it despite the schema
C) The API rejected the tool definition because the name contains special characters, but the error was silently ignored
D) The input_schema is invalid because it has no required array, and the API auto-corrected it to allow empty calls

<details>
<summary>Answer</summary>

**B)** The description is too brief — the model has no way to know a ticker parameter is needed, so it calls the tool with empty input even though the schema could accept it. Descriptions are the single most important factor in tool performance, and the missing ticker context causes the omission. A is wrong because the name pattern `^[a-zA-Z0-9_-]{1,64}$` rejects '!' and the API would return a 400 error — the call would never reach the model at all. C is wrong because the API does not silently ignore tool name validation failures; a 400 error is returned immediately and the call fails. D is wrong because an empty `required` array is valid JSON Schema meaning all properties are optional, so the API does not auto-correct it and the schema is technically sound. (source: Tool use)

</details>

---

## Question 2
You define a tool with input_schema.required = ['location', 'unit'] and unit has enum: ['celsius', 'fahrenheit']. Claude calls the tool with {'location': 'Tokyo', 'unit': 'kelvin'}. What happens?

A) The API accepts the call and passes it to your tool implementation - schema validation only happens for input_examples, not actual tool calls
B) The API rejects the tool call with a 400 error because 'kelvin' is not in the enum
C) Claude receives the tool result and retries with a corrected unit value automatically
D) The model is penalized in its next response but the tool call still executes

<details>
<summary>Answer</summary>

**B)** The API validates every tool call input against the `input_schema` before execution, and 'kelvin' violates the `enum: ['celsius', 'fahrenheit']` constraint, so the request is rejected with a 400 error. A is wrong because schema validation applies to all actual tool calls, not only to `input_examples` — the API enforces the schema on every invocation. C is wrong because Claude does not receive a tool result to reason from; the API rejects the call before execution and your code must handle the error explicitly. D is wrong because there is no penalty mechanism in the API — the call simply fails with a 400 error and no tool result is produced. (source: Tool use)

</details>

---

## Question 3
You have two tools: search_logs ('Search application logs') and query_metrics ('Query system metrics'). In testing, Claude sometimes calls query_metrics when the user asks about error rates in logs. Which fix is most effective?

A) Add input_examples to both tools showing the correct queries for each
B) Update descriptions to clarify data sources: search_logs for text logs, query_metrics for time-series monitoring data
C) Rename the tools to logs_search and metrics_query to follow naming conventions
D) Consolidate both tools into a single query_data tool with a 'data_type' parameter

<details>
<summary>Answer</summary>

**B)** Updating descriptions to name the distinct data sources — text application logs versus time-series monitoring data — directly resolves the ambiguity that causes the wrong tool to be selected, since tool descriptions are the primary signal Claude uses for selection. A is wrong because `input_examples` illustrate parameter shapes for complex inputs but do not disambiguate which tool handles which domain — they cannot fix a selection ambiguity caused by overlapping descriptions. C is wrong because renaming without updating descriptions leaves the same semantic overlap; the model selects based on description content, not name formatting conventions. D is wrong because consolidating two fundamentally different data sources into one tool violates single-responsibility and hides the data-source distinction rather than clarifying it. (source: Tool use)

</details>

---

## Question 4
Your agent has separate tools: create_pr, add_reviewer, merge_pr. In testing, Claude frequently creates a PR but forgets to add reviewers before merging. What's the most effective redesign?

A) Add a system prompt instruction: 'Always add reviewers after creating a PR'
B) Consolidate into a single manage_pr tool with a 'create' action that accepts reviewers
C) Keep the tools separate but add input_examples showing the full create-review-merge workflow
D) Add a validation layer that rejects merge_pr calls if no reviewer was added

<details>
<summary>Answer</summary>

**B)** Consolidating into a single `manage_pr` tool where the 'create' action accepts an optional `reviewers` field makes the reviewer step structurally part of creation, so the model cannot skip it by choosing the wrong next tool. A is wrong because system prompt instructions are probabilistic — the model may still omit the reviewer step when context is long or distracted, and instructions do not enforce sequencing the way tool design does. C is wrong because `input_examples` show parameter shapes but do not constrain which tools the model chooses to call or in what order between three separate tools. D is wrong because a validation layer is a runtime safety net that surfaces errors after the fact rather than eliminating the root cause of the tool-sequencing gap. (source: Tool use)

</details>

---

## Question 5
Your MCP server exposes 12 tools for GitHub operations and 8 for Jira operations. Claude sometimes calls search_issues when the user asks about Jira tickets. Both services have an 'issues' concept. What's the best fix?

A) Add a routing classifier before the MCP server that pre-selects the correct service based on keywords
B) Namespace all tools by service: github_search_issues, jira_search_issues with explicit descriptions
C) Remove the Jira tools from this agent and create a separate Jira-specific agent
D) Add a 'service' parameter to search_issues and let Claude specify which service to query

<details>
<summary>Answer</summary>

**B)** Namespacing tools by service prefix (`github_search_issues`, `jira_search_issues`) combined with explicit per-service descriptions makes selection unambiguous — Anthropic recommends prefix-based namespacing for tools spanning multiple services. A is wrong because an external classifier adds an extra failure surface and can misroute on ambiguous queries, whereas the correct service is already inferable from the tool name and description if namespaced properly. C is wrong because splitting into separate agents removes the ability to coordinate across services in a single workflow, which the user may need. D is wrong because a shared `search_issues` tool with a `service` parameter conflates two distinct services into one tool, violating single-responsibility and requiring Claude to know to pass the right service value every time. (source: Tool use)

</details>

---

## Question 6
You add input_examples to a user-defined tool. Which statement is true about how the API handles them?

A) Input examples are validated against the input_schema, and invalid examples cause a 400 error on the API request
B) Input examples are optional hints that Claude may or may not use, with no validation performed
C) Input examples are only supported for Anthropic-schema tools like web search, not user-defined tools
D) Input examples override the input_schema, allowing Claude to pass values not defined in the schema

<details>
<summary>Answer</summary>

**A)** The API strictly validates `input_examples` against the `input_schema` before processing the request — extra parameters, wrong types, or enum violations all return a 400 error immediately. B is wrong because `input_examples` are not optional hints; they are validated and their valid values are injected into the prompt to guide model behavior. C is wrong because `input_examples` are supported for user-defined tools and Anthropic-schema client tools — they are not available only for server-side tools like web search. D is wrong because examples must conform to the `input_schema` and cannot introduce parameters outside it; the schema always takes precedence. (source: Tool use)

</details>

---

## Question 7
You are building a customer support agent that handles simple, well-defined tasks: looking up orders, checking shipping status, processing returns. Queries are unambiguous and inputs are always provided. What's the optimal model choice?

A) Claude Opus 4.7 - it handles all tool use scenarios best, so it's always the safest choice
B) Claude Sonnet 4.6 - it provides a good balance, and since the tool use is straightforward, there's no downside to using it
C) Claude Haiku - it's fast and cost-effective for straightforward tools, though server-side validation is needed
D) Claude Opus 4.6 - it supports manual budget_tokens control for extended thinking, which is useful even for simple tasks

<details>
<summary>Answer</summary>

**C)** Claude Haiku is optimal for straightforward, unambiguous tool-use tasks — it delivers fast responses at the lowest cost, and since inputs are always provided, its tendency to infer missing parameters is mitigated by server-side validation. A is wrong because Opus 4.7 is designed for complex, ambiguous multi-tool workflows and its additional reasoning capability provides no benefit for simple lookups while adding unnecessary cost and latency. B is wrong because Sonnet 4.6 is more expensive than Haiku for tasks where Haiku performs adequately, making it the wrong cost-performance trade-off. D is wrong because manual `budget_tokens` extended thinking on Opus 4.6 adds latency and cost with zero benefit for simple, deterministic tool calls that require no deep reasoning. (source: Models overview)

</details>

---

## Question 8
Your agent needs to reason about ambiguous user queries (e.g., 'check my account' could mean balance, recent transactions, or settings) and often needs to ask clarifying questions before calling tools. Which model handles this best?

A) Claude Haiku - it is optimized for fast responses and will quickly pick the most likely tool
B) Claude Sonnet 4.6 - it balances speed and reasoning, and supports both adaptive and manual thinking modes
C) Claude Opus 4.7 - it seeks clarification when needed rather than guessing, and handles ambiguous queries best
D) Claude Opus 4.6 - its manual budget_tokens control allows precise tuning of reasoning depth for each query

<details>
<summary>Answer</summary>

**C)** Claude Opus 4.7 is explicitly designed to seek clarification on ambiguous queries rather than guessing, and it achieves the highest accuracy on complex multi-tool scenarios requiring nuanced judgment. A is wrong because Haiku is optimized for speed and may infer missing parameters or pick the most likely tool without asking, which causes incorrect actions on genuinely ambiguous queries. B is wrong because while Sonnet 4.6 supports adaptive thinking, it does not match Opus 4.7's documented strength in recognizing ambiguity and requesting clarification before acting. D is wrong because manual `budget_tokens` mode on Opus 4.6 is deprecated, and tuning a fixed thinking budget does not solve the clarification-seeking behavior gap. (source: Models overview)

</details>

---

## Question 9
You want to force Claude to use the get_weather tool when answering a weather query, AND you need Claude to explain its reasoning in natural language first (e.g., 'Let me check the weather for you'). Extended thinking is enabled. Which approach is optimal?

A) Use tool_choice: {type: 'tool', name: 'get_weather'} - this forces the specific tool while preserving extended thinking
B) Use tool_choice: 'any' - this guarantees a tool is called, and the model can still explain before the tool call
C) Use tool_choice: 'auto' and add instructions in the user message to use the get_weather tool
D) Disable extended thinking temporarily, use tool_choice: 'tool', then re-enable extended thinking in the next turn

<details>
<summary>Answer</summary>

**C)** Using `tool_choice: 'auto'` with explicit user-message instructions is the only valid approach because extended thinking is incompatible with `tool_choice: 'any'` and `tool_choice: {type: 'tool'}` — both return a 400 error when thinking is enabled. A is wrong because `tool_choice: {type: 'tool', name: 'get_weather'}` returns a 400 error when extended thinking is active, making this configuration structurally invalid. B is wrong because `tool_choice: 'any'` also returns a 400 error when extended thinking is enabled, and additionally the API prefills the assistant turn to start a tool call, preventing any natural language explanation before it. D is wrong because you cannot toggle thinking mid-turn, and changing `tool_choice` between turns breaks prompt caching continuity without solving the fundamental incompatibility. (source: Tool use)

</details>

---

## Question 10
In your agentic loop, you check stop_reason to decide whether to execute a tool or return the final response. The API returns stop_reason: 'max_tokens'. What does this indicate and how should you handle it?

A) The model finished its response normally - treat it as end_turn and return the response to the user
B) The model's response was truncated - you should continue the conversation or increase max_tokens
C) The model wants to call a tool but ran out of space to specify which one - terminate and report an error
D) The model encountered an internal error - retry the same request with identical parameters

<details>
<summary>Answer</summary>

**B)** `stop_reason: 'max_tokens'` means the response was cut off at the token limit and is incomplete — the correct action is to continue the conversation by sending the truncated response as context, or increase `max_tokens` to allow a complete response. A is wrong because `max_tokens` is explicitly distinct from `end_turn`, which signals a voluntary stop; treating a truncated response as complete will return an incomplete or corrupt reply to the user. C is wrong because while a truncated tool call is possible, the correct action is continuation or budget increase, not termination — treating this as an unrecoverable error discards a recoverable situation. D is wrong because retrying with identical parameters will produce the same truncated result at the same token boundary without resolving the underlying capacity issue. (source: Tool use)

</details>

---

## Question 11
On Claude Opus 4.7, your code sets thinking: {type: 'enabled', budget_tokens: 12000}. What happens?

A) The API accepts it and Claude uses extended thinking with a 12,000 token budget
B) The API returns a 400 error - Opus 4.7 only supports adaptive thinking
C) The API silently converts the request to adaptive thinking with effort: 'high'
D) The API ignores the thinking config and runs without extended thinking

<details>
<summary>Answer</summary>

**B)** Opus 4.7 only supports adaptive thinking (`type: 'adaptive'`) and explicitly rejects `type: 'enabled'` with a 400 error, because manual `budget_tokens` mode is not available on this model. A is wrong because Opus 4.7 does not support the `'enabled'` thinking type at all — the API rejects the request before any thinking is performed. C is wrong because the API does not silently convert invalid configurations; it returns a hard 400 error requiring the caller to fix the request. D is wrong because the API does not silently ignore an invalid thinking config — it returns a 400 error, not a fallback to no-thinking mode. (source: Extended thinking)

</details>

---

## Question 12
You are building a multi-step agentic workflow where Claude must call tool A, reason about the result, then decide whether to call tool B or C. Which thinking mode is required for Claude to reason between tool calls?

A) Standard extended thinking with budget_tokens - Claude reasons once before all tool calls
B) Interleaved thinking - Claude can reason between tool calls, re-evaluating strategy after each result
C) Disabled thinking - Claude uses its base reasoning capabilities which are sufficient for most workflows
D) Adaptive thinking with effort: 'low' - this minimizes thinking overhead while still allowing tool use

<details>
<summary>Answer</summary>

**B)** Interleaved thinking enables Claude to insert a reasoning step after each tool result, allowing it to re-evaluate strategy and choose the correct next tool based on what was returned — this is the only mode that supports reasoning between individual tool calls. A is wrong because standard extended thinking with `budget_tokens` produces a single thinking block before the first tool call; Claude cannot reason again after seeing a tool result without interleaved mode. C is wrong because base reasoning without any thinking mode does not provide the structured between-call deliberation needed to correctly branch on tool results in complex workflows. D is wrong because `effort: 'low'` in adaptive mode minimizes thinking depth and is designed for simple queries — the opposite of what a branching multi-step workflow requires. (source: Extended thinking)

</details>

---

## Question 13
You switch from manual extended thinking (budget_tokens: 8000) to adaptive thinking on Sonnet 4.6. Which change should you expect in your agentic tool-use workflow?

A) The model will always use exactly 8,000 tokens for thinking, maintaining predictable costs
B) The model will dynamically decide when and how much to think, enabling interleaved reasoning between tool calls
C) The model will skip thinking entirely for simple queries, but complex queries will fail because no budget is specified
D) The model will use the same amount of thinking tokens but bill them at a lower rate

<details>
<summary>Answer</summary>

**B)** Switching to adaptive thinking means the model dynamically decides when to think and how deeply, and interleaved thinking is automatically enabled, allowing reasoning between individual tool calls without any additional configuration. A is wrong because adaptive thinking replaces the fixed `budget_tokens` ceiling with dynamic allocation — there is no guaranteed 8,000-token usage, and costs will vary per request. C is wrong because adaptive thinking never fails on complex queries for lack of a budget; the model allocates thinking tokens as needed up to its internal ceiling. D is wrong because thinking tokens are billed as output tokens regardless of thinking mode — there is no discounted billing rate for adaptive versus manual mode. (source: Extended thinking)

</details>

---

## Question 14
You need interleaved thinking (thinking between tool calls) on Claude Opus 4.6. Which configuration enables this?

A) Manual extended thinking: thinking: {type: 'enabled', budget_tokens: 10000}
B) Adaptive thinking: thinking: {type: 'adaptive'} - interleaved thinking is auto-enabled
C) Disabled thinking - Opus 4.6 always performs interleaved reasoning by default
D) Manual thinking with the interleaved-thinking-2025-05-14 beta header

<details>
<summary>Answer</summary>

**B)** On Claude Opus 4.6, setting `thinking: {type: 'adaptive'}` automatically enables interleaved thinking, which inserts reasoning blocks between each tool call without requiring any additional headers or parameters. A is wrong because manual mode (`type: 'enabled'` with `budget_tokens`) on Opus 4.6 does not support interleaved thinking — reasoning happens once upfront only, and the API does not inject reasoning blocks between tool calls in this mode. C is wrong because Opus 4.6 does not perform interleaved reasoning by default with thinking disabled; base-model reasoning lacks the structured between-call thinking blocks that interleaved mode provides. D is wrong because the `interleaved-thinking-2025-05-14` beta header applies specifically to Sonnet 4.6 manual mode, not to Opus 4.6, and is not the documented path for interleaved thinking on Opus 4.6. (source: Extended thinking)

</details>

---

## Question 15
You set thinking: {type: 'adaptive', display: 'omitted'} to reduce latency. A colleague claims this also reduces costs because thinking tokens are not returned. Is this correct?

A) Yes - omitted display means no thinking tokens are generated or billed
B) No - thinking tokens are still billed internally; omitted display only skips streaming to reduce latency
C) Partially - omitted display reduces costs by about 50% because only half the thinking tokens are billed
D) It depends - costs are reduced only when the model skips thinking entirely for simple queries

<details>
<summary>Answer</summary>

**B)** `display: 'omitted'` only skips streaming the thinking content to the client — the model still generates full thinking tokens internally and you are billed for all of them; the `signature` field in the response still carries the encrypted full thinking. A is wrong because omitting display does not prevent thinking token generation; the model always generates thinking first and the full token count is billed regardless of whether the content is returned. C is wrong because billing is based on all thinking tokens generated, not on a fraction of them — there is no partial billing reduction tied to the display setting. D is wrong because while adaptive thinking may skip thinking for simple queries, that behavior is independent of the `display` field and depends on the model's internal assessment of query complexity, not the display configuration. (source: Extended thinking)

</details>

---

## Question 16
On Claude Opus 4.7, you want to see Claude's summarized thinking process in the API response. What must you do?

A) Nothing - Opus 4.7 defaults to summarized display, so thinking content is automatically included
B) Explicitly set display: 'summarized' because Opus 4.7 defaults to 'omitted'
C) Set display: 'full' to receive the complete unedited thinking text
D) Use manual thinking mode instead of adaptive, because adaptive mode never returns thinking content

<details>
<summary>Answer</summary>

**B)** Opus 4.7 (and Mythos Preview) defaults to `display: 'omitted'`, so you must explicitly set `display: 'summarized'` to receive a summarized thinking block in the API response. A is wrong because `display: 'summarized'` is the default only on Opus 4.6 and Sonnet 4.6 — Opus 4.7's default is 'omitted', so no thinking content is returned without an explicit override. C is wrong because `'full'` is not a valid value for the `display` field — the only supported values are `'summarized'` and `'omitted'`. D is wrong because adaptive mode can return thinking content when `display: 'summarized'` is set; it is manual mode that is unavailable on Opus 4.7, not adaptive mode. (source: Extended thinking)

</details>

---

## Question 17
Your adaptive thinking queries frequently hit stop_reason: 'max_tokens', cutting off responses. You have already increased max_tokens to the maximum your budget allows. What should you adjust?

A) Switch to manual thinking mode with a smaller budget_tokens value for more predictable token usage
B) Lower the effort level (e.g., from 'high' to 'medium') to reduce thinking depth without changing max_tokens
C) Disable thinking entirely - the base model reasoning is sufficient for your use case
D) Add a system prompt instruction telling Claude to use fewer thinking tokens

<details>
<summary>Answer</summary>

**B)** Lowering the `effort` level (e.g., from `'high'` to `'medium'`) reduces the depth of thinking the model performs, which decreases thinking token consumption and leaves more of the `max_tokens` budget for the visible response — this is the documented mechanism for controlling thinking depth in adaptive mode. A is wrong because manual thinking mode is deprecated on 4.6 and rejected on 4.7, and switching to a fixed `budget_tokens` value does not solve a hard `max_tokens` ceiling that has already been maximized. C is wrong because disabling thinking sacrifices reasoning quality across all queries unnecessarily when the problem can be solved by tuning effort level. D is wrong because prompt instructions about token budgets are unreliable guidance that the model may not follow; the `effort` parameter is the intended API-level control for this purpose. (source: Extended thinking)

</details>

---

## Question 18
Which effort level is available on all adaptive thinking models (Opus 4.7, Opus 4.6, Sonnet 4.6, Mythos Preview)?

A) xhigh - it provides the deepest reasoning on all models
B) max, high (default), medium, and low
C) Only high and low - other levels are model-specific
D) max and xhigh - these are the universal high-reasoning levels

<details>
<summary>Answer</summary>

**B)** The four effort levels `max`, `high` (default), `medium`, and `low` are available on every adaptive thinking model — Opus 4.7, Opus 4.6, Sonnet 4.6, and Mythos Preview. A is wrong because `xhigh` is exclusive to Opus 4.7 and is not supported on Opus 4.6, Sonnet 4.6, or Mythos Preview. C is wrong because `max` and `medium` are also universally available, not just `high` and `low` — the full four-level range applies to all adaptive models. D is wrong because `xhigh` is not universal — only `max` is, and combining `max` and `xhigh` as a pair overstates what is broadly supported. (source: Extended thinking)

</details>

---

## Question 19
You provide a custom system prompt and define three tools in your API request. How does the API combine these?

A) Your system prompt replaces the tool-related instructions entirely - you must manually include tool definitions in your prompt
B) The API auto-constructs a system prompt combining tool definitions, your prompt, and tool config
C) Tool definitions are sent as a separate parameter and do not appear in the system prompt at all
D) Your system prompt is appended after the tool definitions, but tool descriptions are truncated to fit within the context window

<details>
<summary>Answer</summary>

**B)** The API automatically constructs a combined system prompt that includes formatting instructions, the full JSON Schema tool definitions, your custom system prompt text, and any tool configuration — this is why well-written tool descriptions directly affect model performance. A is wrong because your custom system prompt does not replace the tool-related instructions; the API merges both, so you never need to manually embed tool definitions in your prompt text. C is wrong because tool definitions do appear in the constructed system prompt in JSON Schema format — they are not kept in a separate, isolated parameter that the model cannot see. D is wrong because tool descriptions are not truncated to fit the context window; they appear in full as part of the auto-constructed prompt. (source: Tool use)

</details>

---

## Question 20
Your tool returns {'uuid': 'a1b2c3...', '256px_image_url': '...', 'mime_type': 'application/pdf'}. You notice Claude sometimes struggles to use these results for follow-up tool calls. What's the most effective improvement?

A) Add more fields to give Claude maximum information and flexibility
B) Replace cryptic identifiers with semantic, human-readable ones: name, image_url, file_type
C) Return raw binary data instead of JSON for better performance
D) The current format is fine - Claude can parse UUIDs and technical identifiers easily

<details>
<summary>Answer</summary>

**B)** Replacing opaque identifiers like `uuid` and `256px_image_url` with semantic names like `name`, `image_url`, and `file_type` directly improves the model's ability to reference and chain these values in follow-up tool calls — Anthropic recommends semantic identifiers over cryptic ones for agentic accuracy. A is wrong because adding more fields increases context token consumption and introduces noise without improving the signal quality that causes the chaining failures. C is wrong because raw binary data is not supported in tool result content — tool responses must be text or structured data. D is wrong because while Claude can technically parse UUIDs, cryptic field names like `256px_image_url` and `mime_type` reduce precision in follow-up calls compared to natural language equivalents. (source: Tool use)

</details>

---

## Question 21
You want to let Claude control whether tool responses are detailed (with all IDs for chaining) or concise (minimal fields). Which pattern does Anthropic recommend?

A) Add a 'verbose' boolean parameter to the tool that toggles between full and minimal output
B) Implement a response_format enum (e.g., 'concise' vs 'detailed') similar to GraphQL field selection
C) Create two separate tools: one that returns detailed output and one that returns concise output
D) Add a 'fields' array parameter where Claude can specify exactly which fields to return

<details>
<summary>Answer</summary>

**B)** A `response_format` enum parameter with values like `'concise'` and `'detailed'` is Anthropic's documented pattern for letting agents control output verbosity — it is explicit, type-safe, and easy for the model to reason about, similar to GraphQL field selection. A is wrong because a boolean `verbose` flag is less expressive than an enum and cannot cleanly support more than two output modes if requirements expand. C is wrong because creating two separate tools for the same operation purely to control verbosity inflates tool count, violates consolidation principles, and degrades selection accuracy. D is wrong because a `fields` array introduces schema complexity and is prone to validation errors when the model specifies field names that don't exactly match the tool's output schema. (source: Tool use)

</details>

---

## Question 22
An agent with access to 18 tools (customer lookup, order management, billing, shipping, returns, reviews) shows degraded tool selection accuracy. According to Anthropic's research, what's the primary issue and fix?

A) The model needs more training data on tool selection - fine-tune it on your specific tool set
B) Agents with too many tools degrade in accuracy; restrict each agent to 4-5 tools per role
C) Add more detailed descriptions to all 18 tools to improve selection accuracy
D) Implement a keyword-based pre-filter that selects 5 candidate tools before each model call

<details>
<summary>Answer</summary>

**B)** Anthropic's research shows tool selection accuracy degrades significantly beyond 4-5 tools per agent — the fix is to split the 18 tools across role-specific agents, each carrying only the tools relevant to its domain. A is wrong because fine-tuning is not the recommended approach for tool selection degradation; restructuring tool count and assignment is the documented solution. C is wrong because better descriptions help with ambiguous descriptions but do not overcome the fundamental decision-complexity problem that arises when the model must choose from 18 candidates. D is wrong because a keyword pre-filter bypasses the model's semantic understanding, can exclude the correct tool on ambiguous queries, and adds architectural complexity that role-based agent splitting avoids. (source: Tool use)

</details>

---

## Question 23
Your team implements list_contacts, list_events, and create_event as three separate tools. The agent frequently calls list_contacts and list_events before every create_event, wasting tokens. What's the recommended fix?

A) Add prompt instructions telling the agent to skip unnecessary listing steps
B) Implement a single schedule_event tool that finds availability and schedules in one call
C) Add caching to the list tools to reduce repeated token costs
D) Remove the list tools - the agent should infer availability from context

<details>
<summary>Answer</summary>

**B)** Implementing a single `schedule_event` tool that internally resolves contacts and checks availability before scheduling consolidates the multi-step workflow into one call, eliminating the unnecessary listing steps by removing the agent's ability to call them independently. A is wrong because prompt instructions cannot reliably prevent the agent from calling tools it deems necessary — the model will continue listing when it believes availability data is stale or missing. C is wrong because caching reduces the token cost of repeated list calls but does not eliminate the unnecessary calls themselves; the workflow inefficiency remains. D is wrong because removing the list tools without replacement forces the agent to guess at availability and contact data, which introduces incorrect event creation rather than solving the problem. (source: Tool use)

</details>

---

## Question 24
You configure tool_choice: 'any' with strict: true on all tool definitions. What guarantees does this combination provide?

A) Claude will call at least one tool, and all tool inputs will strictly follow their input_schema
B) Claude will call ALL available tools in a single response
C) Claude will call exactly one tool, chosen randomly from the available set
D) Claude will call the first tool in the tools array, ensuring deterministic behavior

<details>
<summary>Answer</summary>

**A)** `tool_choice: 'any'` guarantees Claude must call at least one tool from the available set, and `strict: true` on each tool definition guarantees that all generated tool inputs will conform exactly to their `input_schema` without additional or missing fields. B is wrong because `tool_choice: 'any'` means at least one tool must be called — it does not force all tools in the array to be called in a single response. C is wrong because Claude selects the tool(s) based on query semantics and tool descriptions, not through random selection — and `any` allows multiple tool calls, not exactly one. D is wrong because there is no documented behavior where Claude prefers the first tool in the array; tool position in the array does not determine selection order. (source: Tool use)

</details>

---

## Question 25
You are passing conversation history during a multi-turn tool-use workflow with extended thinking. What must you preserve from the assistant's previous turn?

A) Only the text content blocks - thinking blocks contain internal state that should not be exposed
B) Only the tool_use blocks - thinking blocks are regenerated on each turn
C) The complete assistant message including thinking blocks (with signatures) must be preserved
D) Nothing special - extended thinking has no additional requirements for conversation history

<details>
<summary>Answer</summary>

**C)** The complete assistant message — including all thinking blocks with their `signature` fields — must be passed back unchanged in conversation history; the API uses the encrypted signatures to verify reasoning continuity and will reject or mishandle requests where thinking blocks are stripped. A is wrong because thinking blocks are not merely internal state to hide — they are required by the API for multi-turn tool-use continuity, and omitting them breaks the conversation flow. B is wrong because thinking blocks are not regenerated on each turn; they carry forward the reasoning trace from the previous step, and the API expects them verbatim. D is wrong because extended thinking imposes an explicit additional requirement: thinking blocks with signatures must be preserved in the last assistant message when continuing a tool-use conversation. (source: Extended thinking)

</details>

---

## Question 26
What is the key difference between standard extended thinking and interleaved thinking in agentic workflows?

A) Standard thinking uses fewer tokens; interleaved thinking uses more tokens for deeper reasoning
B) Standard thinking reasons once before all tool calls; interleaved thinking allows reasoning between each tool call
C) Standard thinking is only available on Opus; interleaved thinking is available on all models
D) Standard thinking returns visible reasoning; interleaved thinking hides reasoning from the API response

<details>
<summary>Answer</summary>

**B)** Standard extended thinking produces a single reasoning block before the first tool call, while interleaved thinking inserts a fresh reasoning block after each tool result, allowing the model to re-evaluate strategy based on what each tool returned — this is the defining functional difference for multi-step agentic workflows. A is wrong because token usage is determined by query complexity and effort level, not by whether thinking is standard or interleaved — interleaved thinking can use fewer total tokens if the task resolves quickly after the first tool. C is wrong because standard extended thinking (manual mode) is available on Sonnet 4.6 and Opus 4.6, not exclusively on Opus models, and interleaved availability is model-dependent, not universal. D is wrong because reasoning visibility is controlled by the `display` setting (`'summarized'` or `'omitted'`), which applies equally to both standard and interleaved thinking modes. (source: Extended thinking)

</details>

---

## Question 27
You migrate from manual thinking (budget_tokens: 10000) to adaptive thinking on Opus 4.7. How does this affect your ability to predict token costs per request?

A) Costs become more predictable because adaptive thinking uses a fixed default budget
B) Costs become less predictable because Claude dynamically decides thinking depth per request
C) Costs stay the same because adaptive thinking still respects the previous budget_tokens value as a soft limit
D) Costs decrease by exactly 50% because adaptive thinking is more efficient than manual mode

<details>
<summary>Answer</summary>

**B)** Adaptive thinking replaces the fixed `budget_tokens` ceiling with dynamic per-request allocation based on query complexity — costs vary by request and cannot be pre-calculated with certainty, reducing cost predictability compared to manual mode. A is wrong because adaptive thinking has no fixed default budget; it allocates thinking tokens dynamically and the amount varies across requests. C is wrong because adaptive thinking completely ignores any previously used `budget_tokens` value — the parameter does not carry over as a soft limit or reference point. D is wrong because there is no guaranteed 50% cost reduction from switching to adaptive thinking; costs depend entirely on how much thinking each individual query demands. (source: Extended thinking)

</details>

---

## Question 28
In your agentic loop, after processing a tool result, you append both the assistant's tool_use message and the tool result to the conversation history. You then send the next API request. Claude responds with text content but no tool_use block, even though more tools are needed. What might be wrong?

A) The model has reached its max_tokens limit and cannot generate the tool_use block
B) You forgot to set tool_choice: 'any', so Claude decided not to call another tool
C) The tool result wasn't formatted as a tool_result block - the model sees it as user text
D) Claude has reached the end of the task and correctly decided to stop

<details>
<summary>Answer</summary>

**C)** If the tool result is appended as plain user text rather than a properly structured `tool_result` content block with the matching `tool_use_id`, the model treats it as a conversational user message and responds naturally in text rather than continuing the tool-use loop. A is wrong because hitting `max_tokens` produces `stop_reason: 'max_tokens'` with a truncated response — it does not cause Claude to generate fluent text content while silently omitting the tool call. B is wrong because `tool_choice: 'auto'` (the default) should still select additional tools when the conversation history correctly signals an incomplete task; the absence of tool calls despite outstanding work points to a formatting error, not a missing `tool_choice` override. D is wrong because the scenario states more tools are needed — if Claude correctly decided to stop, the task would actually be complete, which contradicts the observed behavior. (source: Tool use)

</details>

---

## Question 29
A developer creates input_examples for a tool but receives a 400 error on the API request. The examples include parameters not defined in the input_schema. Which statement explains this?

A) Input examples are validated against the input_schema, and extra parameters cause a validation error
B) The API rejects examples with extra parameters because they might confuse the model
C) Input examples must be a subset of the input_schema; any deviation returns 400
D) The 400 error is unrelated to examples - it's caused by a malformed JSON payload

<details>
<summary>Answer</summary>

**A)** The API strictly validates `input_examples` against the `input_schema` before processing the request — parameters not defined in the schema are treated as `additionalProperties` violations, causing a 400 error immediately. B is wrong because the rejection is a schema validation failure, not a model-confusion heuristic — the API enforces JSON Schema rules structurally before any model interaction occurs. C is wrong because examples do not need to be a strict subset of parameters; they need to be *valid according to* the schema, meaning they must use defined properties with correct types and enum values. D is wrong because the error is directly caused by the extra parameters in the examples violating schema validation; a malformed JSON payload would produce a different, syntactic parse error. (source: Tool use)

</details>

---

## Question 30
Your agent must coordinate multiple tools in a single workflow: search for documents, extract relevant passages, summarize findings, and email the summary. Queries are often ambiguous. Which model is optimal?

A) Claude Haiku - it's fast enough to handle the multiple tool calls efficiently
B) Claude Sonnet 4.6 - it balances performance and can handle moderate complexity
C) Claude Opus 4.7 - it handles multiple tools best and seeks clarification on ambiguous queries
D) Claude Opus 4.6 - manual budget_tokens control lets you precisely tune reasoning for each step

<details>
<summary>Answer</summary>

**C)** Claude Opus 4.7 is optimal because the workflow requires three capabilities it uniquely provides: coordination across multiple sequential tools, clarification-seeking on ambiguous queries, and auto-enabled interleaved thinking for complex multi-step reasoning between tool calls. A is wrong because Haiku is not designed for complex multi-tool coordination with ambiguous inputs — it may infer missing parameters and make incorrect tool choices rather than asking for clarification. B is wrong because while Sonnet 4.6 handles moderate complexity, it does not match Opus 4.7's documented strength in ambiguity resolution and multi-tool coordination for workflows of this complexity. D is wrong because manual `budget_tokens` mode on Opus 4.6 is deprecated, and the ability to tune a fixed thinking budget does not compensate for Opus 4.6's weaker performance on ambiguous multi-tool workflows compared to Opus 4.7. (source: Models overview)

</details>

---

## Question 31
You set display: 'summarized' and notice the thinking block contains a summary rather than the full reasoning. Which statement about billing is correct?

A) You are billed only for the summarized tokens visible in the response
B) You are billed for the original thinking tokens generated internally, not the summarized output
C) Summarized thinking is free because the summary is generated by a separate process
D) Billing is reduced by 50% because the summary contains half the tokens of the original thinking

<details>
<summary>Answer</summary>

**B)** You are billed for the full original thinking tokens the model generated internally — the summarization is performed by a separate model pass and its token count is not charged, but the underlying thinking tokens always are, regardless of the `display` setting. A is wrong because billing is not based on the summarized output token count visible in the response; the billed count reflects the larger original thinking token generation, which means your invoice will not match the visible token count. C is wrong because while the summarization step itself is not charged, the original thinking tokens that were generated before summarization are always billed as output tokens. D is wrong because there is no guaranteed 50% reduction tied to summarization — billing is based on the actual original thinking token count, which varies by query complexity and bears no fixed ratio to summary length. (source: Extended thinking)

</details>

---
